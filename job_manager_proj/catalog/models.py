from django.db import models


class TypeOfJobs(models.Model):
    name = models.CharField(max_length=40)
    service_descriptions = models.TextField(null=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Types of jobs"


class AbstractAddress(models.Model):
    postal_code = models.CharField(max_length=6)
    region = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(max_length=20, null=True, blank=True)
    locality = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.CharField(max_length=6)
    office_number = models.CharField(max_length=6, null=True, blank=True)
    company = models.OneToOneField(
        "Company", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        addr_fields = (
            self.postal_code,
            self.region,
            self.district,
            self.locality,
            self.street,
            f"д.{self.house_number}",
            self.office_number,
        )
        return ", ".join(field for field in addr_fields if field)

    class Meta:
        abstract = True


class BankBranchAddress(AbstractAddress):
    pass


class RegisteredAddress(AbstractAddress):
    pass


class Signatory(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    basis_for_signing = models.CharField(max_length=150)
    position = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, related_name="signatories", default=None
    )

    def __str__(self):
        return f"{self.position} - {self.name[0]}.{self.patronymic[0]}. {self.surname}"

    def get_short_name(self):
        return f"{self.name[0]}.{self.patronymic[0]}. {self.surname}"

    def save(self, *args, **kwargs):
        if self.is_active:
            Signatory.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class Company(models.Model):
    name = models.CharField(max_length=150)
    unp = models.IntegerField(null=False)
    IBAN = models.CharField(max_length=28)
    bank_name = models.CharField(max_length=50)
    BIC = models.CharField(max_length=11)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "companies"


class Month(models.Model):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    count_of_working_days = models.PositiveIntegerField(null=False)
    number_of_employees = models.FloatField(null=False)
    year = models.PositiveIntegerField(null=True, editable=False)

    def __str__(self):
        return self.start_date.strftime("%b.%y")

    def save(self, *args, **kwargs):
        self.year = self.start_date.year
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(count_of_working_days__lte=31),
                name="month_count_of_working_days_check",
            ),
        ]


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


class HeadOfDepartment(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="heads"
    )

    def __str__(self):
        return str(self.employee)

    class Meta:
        verbose_name_plural = "Heads of departments"


class Department(models.Model):
    name = models.CharField(max_length=50)
    head = models.ForeignKey(
        "HeadOfDepartment",
        on_delete=models.CASCADE,
        related_name="departments",
        null=True,
        blank=True,
    )
    types_of_jobs = models.ManyToManyField(TypeOfJobs, related_name="departments")

    def __str__(self):
        return self.name
