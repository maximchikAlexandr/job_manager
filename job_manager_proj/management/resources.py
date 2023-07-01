from import_export import resources

from management.models import Employee


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
