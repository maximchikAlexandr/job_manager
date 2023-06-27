from django.db import models

from catalog.models import Company, TypeOfJobs, Month


class PlannedBusinessTrip(models.Model):
    day_count = models.IntegerField(null=False, default=1)
    staff_count = models.IntegerField(null=False, default=2)
    lodging_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    public_transportation_fare = models.DecimalField(
        max_digits=14, decimal_places=2, default=0
    )
    one_way_distance_on_company_transport = models.IntegerField(null=True, default=250)
    locality = models.CharField(max_length=50)
    budget_calculation = models.ForeignKey(
        "BudgetCalculation",
        on_delete=models.CASCADE,
        related_name="planned_business_trips",
        null=False,
    )

    def __str__(self):
        return f"{self.locality} - {self.day_count} дня {self.staff_count} чел."


class BudgetCalculation(models.Model):
    workload = models.IntegerField(null=True, default=168)
    hourly_rate = models.DecimalField(max_digits=14, decimal_places=2, default=5.8)
    outsourcing_costs = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    profit = models.IntegerField(null=True, default=25)
    total_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    type_of_jobs = models.ForeignKey(
        TypeOfJobs,
        on_delete=models.CASCADE,
        related_name="agreements",
        null=False,
    )
    commercial_proposal = models.ForeignKey(
        "CommercialProposal",
        on_delete=models.CASCADE,
        related_name="budget_calculations",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.type_of_jobs} - {self.workload} чч."


class CommercialProposal(models.Model):
    service_descriptions = models.TextField(null=False)
    service_delivery_period = models.IntegerField(null=False, default=168)
    total_cost = models.DecimalField(max_digits=14, decimal_places=2)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="commercial_proposals",
        null=False,
    )
    type_of_jobs = models.ForeignKey(
        TypeOfJobs,
        on_delete=models.CASCADE,
        related_name="commercial_proposals",
        null=True,
    )
    service_agreement = models.ForeignKey(
        "ServiceAgreement",
        on_delete=models.CASCADE,
        related_name="commercial_proposals",
        null=True,
        blank=True,
    )

    crm_deal_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.company} - {self.type_of_jobs}"


class ServiceAgreement(models.Model):
    service_descriptions = models.TextField(null=False)
    number = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    date_of_signing = models.DateField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="agreements", null=False
    )

    is_signed = models.BooleanField(default=False, null=False)
    task_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"№{self.number}"


class AgreementStage(models.Model):
    service_descriptions = models.TextField(null=False)
    number = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    service_agreement = models.ForeignKey(
        "ServiceAgreement",
        on_delete=models.CASCADE,
        related_name="agreement_stages",
        null=False,
    )


class ActOfCompletedWork(models.Model):
    COMPLETED = "completed"
    NOT_COMPLETED = "not completed"
    STATUSES = (
        (COMPLETED, "completed"),
        (NOT_COMPLETED, "not completed"),
    )
    status = models.CharField(max_length=20, choices=STATUSES, default=NOT_COMPLETED)
    month_signing_the_act = models.ForeignKey(
        Month,
        on_delete=models.CASCADE,
        related_name="signing_acts",
        null=True,
        blank=True,
    )
    month_of_accounting_act_in_salary = models.ForeignKey(
        Month,
        on_delete=models.CASCADE,
        related_name="acts_in_salary",
        null=True,
        blank=True,
    )
    agreement_stage = models.OneToOneField(
        "AgreementStage", on_delete=models.CASCADE, null=True, blank=True
    )
    service_agreement = models.OneToOneField(
        "ServiceAgreement", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        message = ""
        try:
            message += f"этап №{self.agreement_stage.number}\n"
        except AgreementStage.DoesNotExist:
            message += f"дог. №{self.service_agreement.number}"
        return message

    class Meta:
        verbose_name_plural = "Acts of completed work"
