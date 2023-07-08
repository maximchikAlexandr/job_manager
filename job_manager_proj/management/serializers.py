from rest_framework import serializers

from catalog.models import Department, Month
from management.models import MonthJob


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", 'name']


class YearSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()

    def get_year(self, data):
        return data["month__year"]

    class Meta:
        model = MonthJob
        fields = ('year',)


class MonthInSalarySerializer(serializers.ModelSerializer):
    number_month = month = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()

    def get_number_month(self, obj):
        return obj.month.start_date.month

    def get_month(self, obj):
        return str(obj.month)

    class Meta:
        model = MonthJob
        fields = ("number_month", 'month')


class MonthJobSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    agreement = serializers.SerializerMethodField()

    def get_month(self, obj):
        return str(obj.month)

    def get_employee(self, obj):
        return str(obj.employee)

    def get_company(self, obj):
        return obj.agreement.commercial_proposals.first().company.name

    def get_agreement(self, obj):
        return obj.agreement.number

    class Meta:
        model = MonthJob
        fields = [
            "month", "employee", "company", "agreement", "man_hours",
        ]


class SalarySerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    agreement = serializers.SerializerMethodField()
    hourly_rate = serializers.SerializerMethodField()

    def get_employee(self, obj):
        return str(obj.employee)

    def get_company(self, obj):
        return obj.agreement.commercial_proposals.first().company.name

    def get_agreement(self, obj):
        return obj.agreement.number

    def get_hourly_rate(self, obj):
        return obj.agreement.commercial_proposals.first().budget_calculations.first().hourly_rate

    class Meta:
        model = MonthJob
        fields = [
            "employee", "company", "agreement", "man_hours", "hourly_rate"
        ]
