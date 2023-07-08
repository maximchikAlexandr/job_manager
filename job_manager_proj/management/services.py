from django.db.models import Sum

from catalog.models import Month
from commerce.models import BudgetCalculation, ServiceAgreement


def get_workload_by_agreement_from_calculations(agreement: ServiceAgreement) -> int:
    return BudgetCalculation.objects.filter(
        commercial_proposal__service_agreement=agreement
    ).aggregate(Sum("workload"))["workload__sum"]


def get_planned_workload_by_agreement(agreement: ServiceAgreement) -> int:
    from management.models import MonthJob
    return MonthJob.objects.filter(agreement=agreement).aggregate(Sum("man_hours"))[
        "man_hours__sum"
    ]


def get_planned_workload_by_month(month: Month) -> int:
    from management.models import MonthJob
    return MonthJob.objects.filter(month=month).aggregate(Sum("man_hours"))[
        "man_hours__sum"
    ]


def get_normative_workload_by_month(month: Month) -> int:
    return month.count_of_working_days * 8 * month.number_of_employees
