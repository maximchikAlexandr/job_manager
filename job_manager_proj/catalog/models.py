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
    сompany = models.OneToOneField(
        "Company", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.postal_code}, {self.locality}, {self.street}, д. {self.house_number}-" \
               f" {self.office_number}"

    class Meta:
        abstract = True


class BankBranchAddress(AbstractAddress):
    pass


class RegisteredAddress(AbstractAddress):
    pass


class Company(models.Model):
    name = models.CharField(max_length=150)
    unp = models.IntegerField(null=False)
    IBAN = models.CharField(max_length=28)
    bank_name = models.CharField(max_length=30)
    BIC = models.CharField(max_length=11)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "companies"


class Month(models.Model):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    count_of_working_days = models.IntegerField(null=False)
    number_of_employees = models.FloatField(null=False)

    def __str__(self):
        return self.start_date.strftime("%b.%y")
