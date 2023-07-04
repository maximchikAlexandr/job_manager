from import_export import resources

from catalog.models import Company, Employee, Month



class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company


class MonthResource(resources.ModelResource):
    class Meta:
        model = Month


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
