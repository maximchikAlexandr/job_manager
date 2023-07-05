import decimal
import math

from django.conf import settings
from docxtpl import DocxTemplate


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


def create_service_agreement_file(object_id):
    from commerce.models import ServiceAgreement
    word_template_path = settings.BASE_DIR / "temp/template_service_agreement.docx"
    doc = DocxTemplate(word_template_path)
    agreement = ServiceAgreement.objects.get(pk=object_id)
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
    doc.render(context)
    doc.save(settings.BASE_DIR / f"temp/{context['NUMBER']}.{context['CLIENT_NAME']}.docx")
