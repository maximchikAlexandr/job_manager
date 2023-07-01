from django.contrib.admin import (
    ModelAdmin,
    TabularInline,
    register,
)
from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget
from import_export.admin import ImportExportMixin

from catalog.models import (
    BankBranchAddress,
    Company,
    Month,
    RegisteredAddress,
    TypeOfJobs,
)
from catalog.resources import MonthResource, CompanyResource


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
    save_on_top = True

    class Meta:
        model = Company
        fields = "__all__"


@register(Company)
class CompanyAdmin(ImportExportMixin, ModelAdmin):
    resource_class = CompanyResource
    form = CompanyAdminForm
    inlines = [RegisteredAddressInline, BankBranchAddressInline]
    list_display = ["name"]
    list_per_page = 20


@register(Month)
class MonthAdmin(ImportExportMixin, ModelAdmin):
    resource_class = MonthResource
    list_display = ("month", "year", "count_of_working_days", "number_of_employees")
    list_editable = ("count_of_working_days", "number_of_employees")
    list_per_page = 12
    list_filter = ("year",)

    def month(self, obj):
        return obj.start_date.strftime("%b - %Y")
