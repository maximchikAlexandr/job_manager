import decimal
import math
import os

from django.conf import settings
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
        os.remove(word_template_path)
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
