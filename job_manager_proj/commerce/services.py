import decimal
import math
import os
import requests

from django.conf import settings
from django.db.models import Q
from docxtpl import DocxTemplate
import yadisk


def calc_total_cost(obj):
    planned_business_trips = obj.planned_business_trips.all()
    mileage = 0
    travel_expenses = 0
    if planned_business_trips:
        for trip in planned_business_trips:
            mileage += trip.one_way_distance_on_company_transport
            travel_expenses += (
                    trip.day_count * trip.staff_count * 9
                    + trip.lodging_cost
                    + trip.public_transportation_fare
            )

    salary = math.ceil(obj.workload * obj.hourly_rate)
    income_taxes = math.ceil(decimal.Decimal("0.13") * salary)
    social_security_contributions = math.ceil(decimal.Decimal("0.34") * salary)
    overhead_expenses = math.ceil(decimal.Decimal("1.6") * salary)
    depreciation_expenses = math.ceil(decimal.Decimal("0.175") * salary)
    accident_insurance = math.ceil(decimal.Decimal("0.006") * salary)

    travel_expenses = math.ceil(decimal.Decimal(travel_expenses))
    transportation_expenses = math.ceil(
        decimal.Decimal(mileage) * decimal.Decimal("0.5630625")
    )
    cost_price = (
            salary
            + income_taxes
            + social_security_contributions
            + overhead_expenses
            + depreciation_expenses
            + transportation_expenses
            + accident_insurance
            + travel_expenses
    )
    price_excluding_vat = (
            cost_price * decimal.Decimal((100 + obj.profit) / 100) + obj.outsourcing_costs
    )
    vat = decimal.Decimal("0.2") * price_excluding_vat
    selling_price_including_vat = decimal.Decimal(price_excluding_vat + vat)
    return selling_price_including_vat


def _get_context_by_agreement(agreement):
    company = agreement.commercial_proposals.first().company
    context = {
        "SERVICE_DESCRIPTIONS": agreement.service_descriptions,
        "NUMBER": agreement.number,
        "AMOUNT": agreement.amount,
        "VOT": round(agreement.amount * decimal.Decimal(0.2), 2),
        "DATE_OF_SIGNING": agreement.date_of_signing,
        "CLIENT_NAME": company.name,
        "CLIENT_UNP": company.unp,
        "CLIENT_IBAN": company.IBAN,
        "CLIENT_BANK_NAME": company.bank_name,
        "CLIENT_BIC": company.BIC,
    }
    return context


def _create_document_from_template(
        *, object_id, template_name, output_folder, field_name
):
    from commerce.models import ServiceAgreement

    ydisk = yadisk.YaDisk(token=settings.YANDEX_TOKEN)
    word_template_path = f"{settings.BASE_DIR}/temp/{template_name}"
    ydisk.download(f"/templates/{template_name}", word_template_path)

    doc = DocxTemplate(word_template_path)
    agreement = ServiceAgreement.objects.get(pk=object_id)
    context = _get_context_by_agreement(agreement)
    doc.render(context)

    file_name = f"{context['NUMBER']}.{context['CLIENT_NAME']}.docx"
    local_file_path = f"{settings.BASE_DIR}/temp/{file_name}"
    doc.save(local_file_path)

    remote_folder = f"/{output_folder}/{context['CLIENT_NAME']}"
    if not ydisk.exists(remote_folder):
        ydisk.mkdir(remote_folder)
    remote_file_path = f"{remote_folder}/{file_name}"
    resource_link_obj = ydisk.upload(local_file_path, remote_file_path)
    if resource_link_obj:
        remote_file_path = resource_link_obj.FIELDS["path"]
        remote_file_path = remote_file_path.replace("disk:/", "/disk/")

        setattr(agreement, field_name, remote_file_path)
        agreement.save()
        if os.path.exists(word_template_path):
            os.remove(word_template_path)
        if os.path.exists(local_file_path):
            os.remove(local_file_path)


def create_service_agreement_file(object_id):
    _create_document_from_template(
        object_id=object_id,
        template_name="template_service_agreement.docx",
        output_folder="agreements",
        field_name="agreement_file",
    )


def create_act_file(object_id):
    _create_document_from_template(
        object_id=object_id,
        template_name="template_act.docx",
        output_folder="acts",
        field_name="act_file",
    )


class CRM:
    def __init__(self, hostname, token_for_add, token_for_list):
        self.__hostname = hostname
        self.__token_for_add = token_for_add
        self.__token_for_list = token_for_list

    def add_deal(self, title: str, total_cost: decimal.Decimal) -> int:
        headers = {"Content-Type": "application/json"}
        body = {
            "fields": {
                "TITLE": title,
                "STAGE_ID": "NEW",
                "OPENED": "Y",
                "CURRENCY_ID": "BYN",
                "OPPORTUNITY": total_cost,
            },
            "params": {"REGISTER_SONET_EVENT": "Y"},
        }
        url = (
            f"https://{self.__hostname}/rest/1/{self.__token_for_add}/crm.deal.add.json"
        )
        response = requests.post(url, json=body, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()["result"]
        return {}

    def update_deal(self, id_crm_deal: int, total_cost: decimal.Decimal) -> int:
        headers = {"Content-Type": "application/json"}
        body = {
            "id": id_crm_deal,
            "fields": {"OPPORTUNITY": total_cost},
            "params": {"REGISTER_SONET_EVENT": "Y"},
        }
        url = f"https://{self.__hostname}/rest/1/{self.__token_for_add}/crm.deal.update.json"
        response = requests.post(url, json=body, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()["result"]
        return {}

    def filter_deals_by_stage_id(self, stages):
        headers = {"Content-Type": "application/json"}
        body = {
            "order": {"STAGE_ID": "ASC"},
            "filter": {"=STAGE_ID": stages},
            "select": ["ID", "STAGE_ID"],
        }
        url = f"https://{self.__hostname}/rest/1/{self.__token_for_list}/crm.deal.list.json"
        response = requests.post(url, json=body, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()["result"]
        return {}

def _get_crm():
    return CRM(
        hostname=settings.BX24_HOSTNAME,
        token_for_add=settings.BX24_TOKEN_ADD,
        token_for_list=settings.BX24_TOKEN_LIST,
    )


def create_crm_deal(cp_id: int):
    from commerce.models import CommercialProposal

    proposal = CommercialProposal.objects.get(pk=cp_id)
    crm = _get_crm()
    id_crm_deal = crm.add_deal(
        title=proposal.company.name, total_cost=float(proposal.total_cost)
    )
    proposal.crm_deal_id = id_crm_deal
    proposal.save()


def update_cost_in_crm_deal(id_crm_deal: int, total_cost: decimal.Decimal):
    _get_crm().update_deal(id_crm_deal=id_crm_deal, total_cost=float(total_cost))


def check_deal_stage():
    from commerce.models import CommercialProposal

    stages = ["PREPARATION", "EXECUTING"]
    deals = _get_crm().filter_deals_by_stage_id(stages)

    # create_service_agreement_file
    preparation_deals = [deal["ID"] for deal in deals if deal["STAGE_ID"] == "PREPARATION"]
    proposals = CommercialProposal.objects.filter(
        Q(crm_deal_id__in=preparation_deals) & Q(service_agreement__agreement_file=None)
    )
    for proposal in proposals:
        if proposal.service_agreement.id:
            create_service_agreement_file(proposal.service_agreement.id)

    # service_agreement.is_signed = True
    executing_deals= [
        deal["ID"] for deal in deals if deal["STAGE_ID"] == "EXECUTING"
    ]
    proposals = CommercialProposal.objects.filter(
        Q(crm_deal_id__in=executing_deals) & Q(service_agreement__is_signed=False)
    )
    for proposal in proposals:
        proposal.service_agreement.is_signed = True
        proposal.service_agreement.save()
