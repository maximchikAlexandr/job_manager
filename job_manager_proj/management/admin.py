from django.contrib.admin import (
    ModelAdmin,
    register,
)
from import_export.admin import ImportExportMixin


from management.models import (
    Department,
    Employee,
    HeadOfDepartment,
    MonthJob,
)
from management.resources import EmployeeResource


@register(MonthJob)
class MonthJobAdmin(ModelAdmin):
    list_display = ["company", "man_hours", "employee", "month"]
    list_editable = ["man_hours", "employee", "month"]

    def company(self, obj):
        return obj.act.agreement.company


@register(Employee)
class EmployeeAdmin(ImportExportMixin, ModelAdmin):
    resource_class = EmployeeResource
    list_display = ["surname", "name", "patronymic", "rate"]
    list_editable = ["rate"]


@register(Department)
class DepartmentAdmin(ModelAdmin):
    list_display = ["name", "head"]


@register(HeadOfDepartment)
class DHeadOfDepartmentAdmin(ModelAdmin):
    list_display = ["employee"]
