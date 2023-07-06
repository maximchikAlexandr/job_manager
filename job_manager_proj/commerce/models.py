from catalog.models import Company, Month, TypeOfJobs
from commerce.services import calc_total_cost
from django.db import models


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
        return f"{self.locality} - {self.day_count} дн. {self.staff_count} чел."


class BudgetCalculation(models.Model):
    workload = models.IntegerField(null=True, default=168)
    hourly_rate = models.DecimalField(max_digits=14, decimal_places=2, default=5.8)
    outsourcing_costs = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    profit = models.IntegerField(null=True, default=25)
    total_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    type_of_jobs = models.ForeignKey(
        TypeOfJobs,
        on_delete=models.CASCADE,
        related_name="budget_calculations",
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
        return f"{self.type_of_jobs} - {self.workload} чч. - {self.total_cost} р."

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        new_total_cost = calc_total_cost(self)
        if self.total_cost != new_total_cost:
            self.total_cost = new_total_cost
        super().save(*args, **kwargs)

        if self.commercial_proposal:
            self.commercial_proposal.save()


class CommercialProposal(models.Model):
    service_descriptions = models.TextField(null=False, blank=True)
    service_delivery_period = models.IntegerField(null=False, default=60)
    total_cost = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="commercial_proposals",
        null=False,
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
        return f"{self.company} - {self.total_cost} р. - {self.service_delivery_period} дн."

    def save(self, *args, **kwargs):
        if self.pk:
            total_cost = 0
            for calculation in self.budget_calculations.all():
                total_cost += calculation.total_cost
            if self.total_cost != total_cost:
                self.total_cost = total_cost
        super().save(*args, **kwargs)
        if self.service_agreement:
            self.service_agreement.save()


class ServiceAgreement(models.Model):
    COMPLETED = "completed"
    NOT_COMPLETED = "not completed"
    STATUSES = (
        (COMPLETED, "completed"),
        (NOT_COMPLETED, "not completed"),
    )
    service_descriptions = models.TextField(null=False)
    number = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    date_of_signing = models.DateField()
    is_signed = models.BooleanField(default=False, null=False)
    task_id = models.IntegerField(null=True, blank=True)
    act_status = models.CharField(max_length=20, choices=STATUSES, default=NOT_COMPLETED)
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
    agreement_file = models.CharField(max_length=256, null=True, blank=True)
    act_file = models.CharField(max_length=256, null=True, blank=True)
    def __str__(self):
        return f"№{self.number} - {self.amount} р."

    def save(self, *args, **kwargs):
        if self.pk:
            total_cost = 0
            for proposal in self.commercial_proposals.all():
                total_cost += proposal.total_cost
            if self.amount != total_cost:
                self.amount = total_cost
        super().save(*args, **kwargs)
