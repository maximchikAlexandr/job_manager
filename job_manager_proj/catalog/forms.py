from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget


from catalog.models import Company


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
