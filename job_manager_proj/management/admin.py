from django.contrib.admin import (
    ModelAdmin,
    register,
)


from management.models import (
    Department,
    Employee,
    HeadOfDepartment,
    MonthJob,
)


@register(MonthJob)
class MonthJobAdmin(ModelAdmin):
    list_display = ["company", "man_hours", "employee", "month"]
    list_editable = ["man_hours", "employee", "month"]

    def company(self, obj):
        return obj.act.agreement.company

    # def save_model(
    #     self,
    #     request: WSGIRequest,
    #     obj: MonthJob,
    #     form: "MonthJobAdminWorkForm",
    #     change: bool,
    # ):
    #     obj.save()
    #
    #     hour_validator = ActOfCompletedWorkValidator(obj.act)
    #     if not hour_validator.has_valid_sum():
    #         hour_validator.send_error_message(request)


@register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = ["surname", "name", "patronymic", "rate"]
    list_editable = ["rate"]


@register(Department)
class DepartmentAdmin(ModelAdmin):
    list_display = ["name", "head"]


@register(HeadOfDepartment)
class DHeadOfDepartmentAdmin(ModelAdmin):
    list_display = ["employee"]

