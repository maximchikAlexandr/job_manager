from catalog.models import (
    Company,
    Month
)
from import_export import resources


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company


class MonthResource(resources.ModelResource):
    class Meta:
        model = Month
