from django.contrib.admin import (
    ModelAdmin,
    TabularInline,
    models,
    register,
)
from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget

from catalog.models import (
    BankBranchAddress,
    Company,
    Month,
    RegisteredAddress,
    TypeOfJobs,
)


class AbstractModelAdmin(ModelAdmin):
    def get_logs_by(self, obj):
        return models.LogEntry.objects.filter(
            object_id=obj.pk, content_type__model=self.opts.model_name
        )

    def author(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).first(), "user", None)
        return "unknown"

    def editor(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).last(), "user", None)
        return "unknown"

    def created(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).first(), "action_time", None)
        return "unknown"

    def edited(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).last(), "action_time", None)
        return "unknown"


@register(TypeOfJobs)
class TypeOfJobsAdmin(ModelAdmin):
    list_display = ["name"]


class AddressTabularInline(TabularInline):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "postal_code":
            field.widget.attrs["style"] = "width: 100px;"
        elif db_field.name == "region":
            field.widget.attrs["style"] = "width: 150px;"
        elif db_field.name == "district":
            field.widget.attrs["style"] = "width: 150px;"
        elif db_field.name == "locality":
            field.widget.attrs["style"] = "width: 150px;"
        elif db_field.name == "street":
            field.widget.attrs["style"] = "width: 250px;"
        elif db_field.name == "house_number":
            field.widget.attrs["style"] = "width: 50px;"
        elif db_field.name == "office_number":
            field.widget.attrs["style"] = "width: 50px;"
        return field


class RegisteredAddressInline(AddressTabularInline):
    model = RegisteredAddress


class BankBranchAddressInline(AddressTabularInline):
    model = BankBranchAddress


class CompanyAdminForm(forms.ModelForm):
    name = forms.CharField(
        widget=AdminTextInputWidget(attrs={"class": "name", "style": "width: 400px;"})
    )
    unp = forms.CharField(
        widget=AdminTextInputWidget(attrs={"class": "unp", "style": "width: 260px;"})
    )

    class Meta:
        model = Company
        fields = "__all__"


@register(Company)
class CompanyAdmin(ModelAdmin):
    form = CompanyAdminForm
    inlines = [RegisteredAddressInline, BankBranchAddressInline]
    list_display = ["name"]


@register(Month)
class MonthAdmin(ModelAdmin):
    list_display = [
        "month",
        "count_of_working_days",
        "number_of_employees",
    ]
    list_editable = [
        "count_of_working_days",
        "number_of_employees",
    ]
    list_per_page = 12

    def month(self, obj):
        return obj.start_date.strftime("%b - %Y")
