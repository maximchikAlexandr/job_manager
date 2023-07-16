from django.db import models

from catalog.models import Company, Month, TypeOfJobs
from commerce.services import calc_total_cost
from commerce.tasks import update_cost_in_crm_deal_task


class PlannedBusinessTrip(models.Model):
    day_count = models.PositiveIntegerField(null=False, default=1)
    staff_count = models.PositiveIntegerField(null=False, default=2)
    lodging_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    public_transportation_fare = models.DecimalField(
        max_digits=14, decimal_places=2, default=0
    )
    one_way_distance_on_company_transport = models.PositiveIntegerField(null=True, default=250)
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
    workload = models.PositiveIntegerField(null=True, default=168)
    hourly_rate = models.DecimalField(max_digits=14, decimal_places=2, default=5.8)
    outsourcing_costs = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    profit = models.PositiveIntegerField(null=True, default=25)
    # calculated fields
    salary = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    income_taxes = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    social_security_contributions = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    overhead_expenses = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    depreciation_expenses = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    accident_insurance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    travel_expenses = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    transportation_expenses = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cost_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    price_excluding_vat = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=14, decimal_places=2, default=0)
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

        calc_res = calc_total_cost(self)
        if self.total_cost != calc_res["total_cost"]:
            for field_name, field_val in calc_res.items():
                setattr(self, field_name, field_val)
        super().save(*args, **kwargs)

        if self.commercial_proposal:
            self.commercial_proposal.save()


class CommercialProposal(models.Model):
    service_descriptions = models.TextField(null=False, blank=True)
    service_delivery_period = models.PositiveIntegerField(null=False, default=60)
    total_cost = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    advance_payment_percentage = models.PositiveIntegerField(null=False, default=50)
    advance_payment_deadline = models.PositiveIntegerField(null=False, default=15)
    payment_deferral = models.PositiveIntegerField(null=False, default=30)
    crm_deal_id = models.PositiveIntegerField(null=True, blank=True)
    proposal_file = models.CharField(max_length=256, null=True, blank=True)
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

    def __str__(self):
        return f"{self.company} - {self.total_cost} р. - {self.service_delivery_period} дн."

    def save(self, *args, **kwargs):
        if self.pk:
            total_cost = 0
            for calculation in self.budget_calculations.all():
                total_cost += calculation.total_cost
            if self.total_cost != total_cost:
                self.total_cost = total_cost
                if self.crm_deal_id:
                    update_cost_in_crm_deal_task.delay(self.crm_deal_id, total_cost)
        super().save(*args, **kwargs)
        if self.service_agreement:
            self.service_agreement.save()


class ServiceAgreement(models.Model):
    service_descriptions = models.TextField(null=True, blank=True)
    number = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    date_of_signing = models.DateField()
    is_signed = models.BooleanField(default=False, null=False)
    task_id = models.IntegerField(null=True, blank=True)
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
