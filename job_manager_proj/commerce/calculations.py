import decimal
import math


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
    selling_price_including_vat = price_excluding_vat + vat
    obj.total_cost = selling_price_including_vat
    return obj
