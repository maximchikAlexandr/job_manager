import math
import os
from datetime import datetime
from decimal import Decimal

import requests
import yadisk
from django.conf import settings
from django.db.models import F, Q, Sum
from django.db.models.functions import Ceil
from docxtpl import DocxTemplate


def calc_total_cost(obj):
    from commerce.models import BudgetCalculation, PlannedBusinessTrip

    trips_data = PlannedBusinessTrip.objects.filter(budget_calculation=obj).aggregate(
        travel_expenses=Ceil(
            Sum(
                F("day_count") * F("staff_count") * 9
                + F("lodging_cost")
                + F("public_transportation_fare")
            )
        ),
        mileage=Sum(F("one_way_distance_on_company_transport")),
    )

    calc_input_data = (
        BudgetCalculation.objects.filter(id=obj.pk)
        .values(
            "workload",
            "hourly_rate",
            "profit_percentage",
            "outsourcing_costs",
        )
        .first()
    )
    calc_res = {}
    calc_res["salary"] = math.ceil(
        calc_input_data["workload"] * calc_input_data["hourly_rate"]
    )
    calc_res["income_taxes"] = math.ceil(Decimal("0.13") * calc_res["salary"])
    calc_res["social_security_contributions"] = math.ceil(
        Decimal("0.34") * calc_res["salary"]
    )
    calc_res["overhead_expenses"] = math.ceil(Decimal("1.6") * calc_res["salary"])
    calc_res["depreciation_expenses"] = math.ceil(Decimal("0.175") * calc_res["salary"])
    calc_res["accident_insurance"] = math.ceil(Decimal("0.006") * calc_res["salary"])

    calc_res["travel_expenses"] = Decimal(trips_data["travel_expenses"])
    calc_res["transportation_expenses"] = math.ceil(
        Decimal(trips_data["mileage"]) * Decimal("0.5630625")
    )
    calc_res["cost_price"] = (
        calc_res["salary"]
        + calc_res["income_taxes"]
        + calc_res["social_security_contributions"]
        + calc_res["overhead_expenses"]
        + calc_res["depreciation_expenses"]
        + calc_res["transportation_expenses"]
        + calc_res["accident_insurance"]
        + calc_res["travel_expenses"]
    )
    calc_res["profit"] = calc_res["cost_price"] * Decimal(
        calc_input_data["profit_percentage"] / 100
    )
    calc_res["price_excluding_vat"] = (
        calc_res["cost_price"]
        + calc_res["profit"]
        + calc_input_data["outsourcing_costs"]
    )
    calc_res["price_excluding_vat"] = round(calc_res["price_excluding_vat"], 2)
    calc_res["vat"] = round(Decimal("0.2") * calc_res["price_excluding_vat"], 2)
    calc_res["total_cost"] = Decimal(calc_res["price_excluding_vat"] + calc_res["vat"])
    return calc_res


def _create_document_from_template(
    *, object_id, template_name, output_folder, field_name, context_source, model
):
    ydisk = yadisk.YaDisk(token=settings.YANDEX_TOKEN)
    word_template_path = f"{settings.BASE_DIR}/temp/{template_name}"
    ydisk.download(f"/templates/{template_name}", word_template_path)

    doc = DocxTemplate(word_template_path)
    model_instance = model.objects.get(pk=object_id)
    context = context_source(model_instance)
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

        setattr(model_instance, field_name, remote_file_path)
        model_instance.save()
        if os.path.exists(word_template_path):
            os.remove(word_template_path)
        if os.path.exists(local_file_path):
            os.remove(local_file_path)


def _get_context_by_agreement(agreement):
    proposal = agreement.commercial_proposals.first()
    company = proposal.company
    signatory = company.signatories.filter(is_active=True).first()
    context = {
        "SERVICE_DESCRIPTIONS": agreement.service_descriptions,
        "SERVICE_DELIVERY_PERIOD": proposal.service_delivery_period,
        "ADVANCE_PAYMENT_PERCENTAGE": proposal.advance_payment_percentage,
        "REMAINING_PAYMENT_PERCENTAGE": 100 - proposal.advance_payment_percentage,
        "ADVANCE_PAYMENT_DEADLINE": proposal.advance_payment_deadline,
        "PAYMENT_DEFERRAL": proposal.payment_deferral,
        "NUMBER": agreement.number,
        "AMOUNT": agreement.amount,
        "VOT": round(agreement.amount * Decimal(0.2), 2),
        "DATE_OF_SIGNING": agreement.date_of_signing.strftime("%d.%m.%Y"),
        "CLIENT_NAME": company.name,
        "CLIENT_UNP": company.unp,
        "CLIENT_ADDRESS": str(company.registeredaddress),
        "CLIENT_IBAN": company.IBAN,
        "CLIENT_BANK_NAME": company.bank_name,
        "CLIENT_BIC": company.BIC,
        "CLIENT_BANK_ADDRESS": str(company.bankbranchaddress),
        "SIGNATORY_NAME": signatory.name,
        "SIGNATORY_SURNAME": signatory.surname,
        "SIGNATORY_PATRONYMIC": signatory.patronymic,
        "SIGNATORY_BASIS_FOR_SIGNING": signatory.basis_for_signing,
        "SIGNATORY_POSITION": signatory.position,
        "SIGNATORY_SHORT_NAME": signatory.get_short_name(),
    }
    return context


def _get_context_by_proposal(proposal):
    budget_calc = proposal.budget_calculations.first()
    context = {
        "CUR_DATE": datetime.today().strftime("%d.%m.%Y"),
        "CLIENT_NAME": proposal.company.name,
        "SERVICE_DESCRIPTIONS": proposal.service_descriptions,
        "SERVICE_PRICE_EXCLUDING_VAT": budget_calc.price_excluding_vat,
        "SERVICE_VAT": budget_calc.vat,
        "SERVICE_TOTAL_COST": budget_calc.total_cost,
        "SERVICE_DELIVERY_PERIOD": proposal.service_delivery_period,
        "ADVANCE_PAYMENT_PERCENTAGE": proposal.advance_payment_percentage,
        "REMAINING_PAYMENT_PERCENTAGE": 100 - proposal.advance_payment_percentage,
        "ADVANCE_PAYMENT_DEADLINE": proposal.advance_payment_deadline,
        "PAYMENT_DEFERRAL": proposal.payment_deferral,
        "NUMBER": f"{datetime.today().strftime('%Y-%m')}-1",
    }
    return context


def _get_context_by_calculation(calculation):
    context = {
        "CLIENT_NAME": calculation.commercial_proposal.company.name,
        "SERVICE_DESCRIPTIONS": calculation.commercial_proposal.service_descriptions,
        "SERVICE_WORKLOAD": calculation.workload,
        "SERVICE_HOURLY_RATE": calculation.hourly_rate,
        "SERVICE_SALARY": calculation.salary,
        "SERVICE_SOCIAL_SECURITY_CONTRIBUTIONS": calculation.social_security_contributions
        + calculation.income_taxes,
        "SERVICE_OVERHEAD_EXPENSES": calculation.overhead_expenses,
        "SERVICE_DEPRECIATION_EXPENSES": calculation.depreciation_expenses,
        "SERVICE_TRANSPORTATION_EXPENSES": calculation.transportation_expenses,
        "SERVICE_ACCIDENT_INSURANCE": calculation.accident_insurance,
        "SERVICE_TRAVEL_EXPENSES": calculation.travel_expenses,
        "SERVICE_COST_PRICE": calculation.cost_price,
        "SERVICE_PROFIT": calculation.profit,
        "SERVICE_OUTSOURCING_COSTS": calculation.outsourcing_costs,
        "SERVICE_PRICE_EXCLUDING_VAT": calculation.price_excluding_vat,
        "SERVICE_VAT": calculation.vat,
        "SERVICE_TOTAL_COST": calculation.total_cost,
        "NUMBER": datetime.today().strftime("%d-%m-%Y"),
    }
    return context


def create_service_agreement_file(object_id):
    from commerce.models import ServiceAgreement

    _create_document_from_template(
        object_id=object_id,
        template_name="template_agreement.docx",
        output_folder="agreements",
        field_name="agreement_file",
        context_source=_get_context_by_agreement,
        model=ServiceAgreement,
    )


def create_act_file(object_id):
    from commerce.models import ServiceAgreement

    _create_document_from_template(
        object_id=object_id,
        template_name="template_act.docx",
        output_folder="acts",
        field_name="act_file",
        context_source=_get_context_by_agreement,
        model=ServiceAgreement,
    )


def create_proposal_file(object_id):
    from commerce.models import CommercialProposal

    _create_document_from_template(
        object_id=object_id,
        template_name="template_commercial_proposal.docx",
        output_folder="commercial_proposals",
        field_name="proposal_file",
        context_source=_get_context_by_proposal,
        model=CommercialProposal,
    )


def create_calculation_file(object_id):
    from commerce.models import BudgetCalculation

    _create_document_from_template(
        object_id=object_id,
        template_name="template_budget_calculation.docx",
        output_folder="budget_calculations",
        field_name="calculation_file",
        context_source=_get_context_by_calculation,
        model=BudgetCalculation,
    )


class CRM:
    def __init__(self, hostname, token_for_add, token_for_list):
        self.__hostname = hostname
        self.__token_for_add = token_for_add
        self.__token_for_list = token_for_list

    def add_deal(self, title: str, total_cost: Decimal) -> int:
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

    def update_deal(self, id_crm_deal: int, total_cost: Decimal) -> int:
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


def update_cost_in_crm_deal(id_crm_deal: int, total_cost: Decimal):
    _get_crm().update_deal(id_crm_deal=id_crm_deal, total_cost=float(total_cost))


def check_deal_stage():
    from commerce.models import CommercialProposal

    stages = ["PREPARATION", "EXECUTING"]
    deals = _get_crm().filter_deals_by_stage_id(stages)

    # create_service_agreement_file
    preparation_deals = [
        deal["ID"] for deal in deals if deal["STAGE_ID"] == "PREPARATION"
    ]
    proposals = CommercialProposal.objects.filter(
        Q(crm_deal_id__in=preparation_deals) & Q(service_agreement__agreement_file=None)
    )
    for proposal in proposals:
        if proposal.service_agreement.id:
            create_service_agreement_file(proposal.service_agreement.id)

    # service_agreement.is_signed = True
    executing_deals = [deal["ID"] for deal in deals if deal["STAGE_ID"] == "EXECUTING"]
    proposals = CommercialProposal.objects.filter(
        Q(crm_deal_id__in=executing_deals) & Q(service_agreement__is_signed=False)
    )
    for proposal in proposals:
        proposal.service_agreement.is_signed = True
        proposal.service_agreement.save()
