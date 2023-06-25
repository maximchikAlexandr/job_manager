from django.db import models


# ________________________________________________________________
# Catalog
class TypeOfJobs(models.Model):
    name = models.CharField(max_length=40)
    service_descriptions = models.TextField(null=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "catalog_type_of_jobs"


class AbstractAddress(models.Model):
    postal_code = models.CharField(max_length=6)
    region = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(max_length=20, null=True, blank=True)
    locality = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.CharField(max_length=6)
    office_number = models.CharField(max_length=6, null=True, blank=True)
    сompany = models.OneToOneField(
        "Company", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.postal_code}, {self.locality}, {self.street}, д. {self.house_number}-" \
               f" {self.office_number}"

    class Meta:
        abstract = True


class BankBranchAddress(AbstractAddress):
    class Meta:
        db_table = "catalog_bank_branch_address"


class RegisteredAddress(AbstractAddress):
    class Meta:
        db_table = "catalog_registered_address"


class Company(models.Model):
    name = models.CharField(max_length=150)
    unp = models.IntegerField(null=False)
    IBAN = models.CharField(max_length=28)
    bank_name = models.CharField(max_length=30)
    BIC = models.CharField(max_length=11)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "catalog_company"
        verbose_name_plural = "companies"


class Month(models.Model):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    count_of_working_days = models.IntegerField(null=False)
    number_of_employees = models.FloatField(null=False)

    def __str__(self):
        return self.start_date.strftime("%b.%y")

    class Meta:
        db_table = "catalog_month"


# ________________________________________________________________
# Commerce
class PlannedBusinessTrip(models.Model):
    day_count = models.IntegerField(null=False, default=1)
    staff_count = models.IntegerField(null=False, default=2)
    lodging_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    public_transportation_fare = models.DecimalField(max_digits=14, decimal_places=2, default=0)
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

    class Meta:
        db_table = "commerce_planned_business_trip"


class BudgetCalculation(models.Model):
    workload = models.IntegerField(null=True, default=168)
    hourly_rate = models.DecimalField(max_digits=14, decimal_places=2, default=5.8)
    outsourcing_costs = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    profit = models.IntegerField(null=True, default=25)
    total_cost = models.DecimalField(max_digits=14, decimal_places=2)
    type_of_jobs = models.ForeignKey(
        "TypeOfJobs",
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

    class Meta:
        db_table = "commerce_budget_calculation"


class CommercialProposal(models.Model):
    service_descriptions = models.TextField(null=False)
    service_delivery_period = models.IntegerField(null=False, default=168)
    total_cost = models.DecimalField(max_digits=14, decimal_places=2)
    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="commercial_proposals",
        null=False,
    )
    type_of_jobs = models.ForeignKey(
        "TypeOfJobs",
        on_delete=models.CASCADE,
        related_name="commercial_proposals",
        null=True,
    )
    service_agreement = models.ForeignKey(
        "ServiceAgreement",
        on_delete=models.CASCADE,
        related_name="commercial_proposals",
        null=True, blank=True
    )

    crm_deal_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.company} - {self.type_of_jobs}"

    class Meta:
        db_table = "commerce_commercial_proposal"


class ServiceAgreement(models.Model):
    service_descriptions = models.TextField(null=False)
    number = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    date_of_signing = models.DateField()
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, related_name="agreements", null=False
    )

    is_signed = models.BooleanField(default=False, null=False)
    task_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"№{self.number}"

    class Meta:
        db_table = "commerce_service_agreement"


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

    class Meta:
        db_table = "commerce_agreement_stage"


class ActOfCompletedWork(models.Model):
    COMPLETED = "completed"
    NOT_COMPLETED = "not completed"
    STATUSES = (
        (COMPLETED, "completed"),
        (NOT_COMPLETED, "not completed"),
    )
    status = models.CharField(max_length=20, choices=STATUSES, default=NOT_COMPLETED)
    month_signing_the_act = models.ForeignKey(
        "Month",
        on_delete=models.CASCADE,
        related_name="signing_acts",
        null=True,
        blank=True,
    )
    month_of_accounting_act_in_salary = models.ForeignKey(
        "Month",
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
        db_table = "commerce_act_of_completed_work"


# ________________________________________________________________
# Management
class MonthJob(models.Model):
    PRODUCED = "produced"
    PLANNED = "planned"
    STATUSES = (
        (PRODUCED, "produced"),
        (PLANNED, "planned"),
    )
    man_hours = models.FloatField(null=False)
    employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name="jobs"
    )
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name="jobs")
    status = models.CharField(max_length=20, choices=STATUSES, default=PLANNED)
    agreement = models.ForeignKey(
        ServiceAgreement, on_delete=models.CASCADE, related_name="jobs"
    )

    def __str__(self):
        return f"{self.employee} - {self.act} - {self.month}"

    class Meta:
        db_table = "management_month_job"


class Employee(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    rate = models.FloatField(null=False)
    id_in_task_manager = models.CharField(max_length=36, null=False, blank=True)
    department = models.ForeignKey(
        "Department",
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name[0]}.{self.patronymic[0]}. {self.surname}"

    class Meta:
        db_table = "management_employee"


class Department(models.Model):
    name = models.CharField(max_length=20)
    head = models.ForeignKey(
        "HeadOfDepartment",
        on_delete=models.CASCADE,
        related_name="departments",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "management_department"


class HeadOfDepartment(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="heads"
    )

    def __str__(self):
        return str(self.employee)

    class Meta:
        db_table = "management_head_of_department"
