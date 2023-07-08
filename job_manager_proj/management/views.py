from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Department
from django.db.models import Q
from management.models import MonthJob
from management.serializers import (
    DepartmentSerializer,
    MonthJobSerializer,
    YearInMonthJobSerializer,
    MonthInSalarySerializer,
    SalarySerializer,
)


# Report "MonthJob"
class DepartmentInMonthJobAPIView(ListAPIView):
    queryset = Department.objects.filter(employees__jobs__isnull=False).distinct()
    serializer_class = DepartmentSerializer


class YearInMonthJobListAPIView(APIView):
    def post(self, request):
        id_departament = request.data["id_departament"]
        queryset = (
            MonthJob.objects.filter(employee__department__id=id_departament)
            .values("month__year")
            .distinct()
        )
        serializer = YearInMonthJobSerializer(queryset, many=True)
        return Response(serializer.data)


class MonthJobListAPIView(APIView):
    def post(self, request):
        year = request.data["year"]
        id_departament = request.data["id_departament"]
        queryset = MonthJob.objects.filter(
            Q(month__year=year) & Q(employee__department__id=id_departament)
        ).order_by("month__start_date")
        serializer = MonthJobSerializer(queryset, many=True)
        return Response(serializer.data)


# Report "Salary"
class DepartmentSalaryJobAPIView(ListAPIView):
    queryset = Department.objects.filter(
        Q(employees__jobs__isnull=False) & Q(employees__jobs__status="produced")
    ).distinct()
    serializer_class = DepartmentSerializer


class YearInSalaryListAPIView(APIView):
    def post(self, request):
        id_departament = request.data["id_departament"]
        queryset = (
            MonthJob.objects.filter(
                Q(employee__department__id=id_departament) & Q(status="produced")
            )
            .values("month__year")
            .distinct()
        )
        serializer = YearInMonthJobSerializer(queryset, many=True)
        return Response(serializer.data)


class MonthInSalaryListAPIView(APIView):
    def post(self, request):
        year = request.data["year"]
        id_departament = request.data["id_departament"]
        queryset = (
            MonthJob.objects.filter(
                Q(employee__department__id=id_departament)
                & Q(status="produced")
                & Q(month__year=year)
            )
            .distinct()
            .order_by("month__start_date")
        )
        serializer = MonthInSalarySerializer(queryset, many=True)
        return Response(serializer.data)


class SalaryListAPIView(APIView):
    def post(self, request):
        number_month = request.data["number_month"]
        year = request.data["year"]
        id_departament = request.data["id_departament"]
        queryset = (
            MonthJob.objects.filter(
                Q(employee__department__id=id_departament)
                & Q(status="produced")
                & Q(month__year=year)
                & Q(month__start_date__month=number_month)
            )
            .distinct()
            .order_by("employee__name")
        )
        serializer = SalarySerializer(queryset, many=True)
        return Response(serializer.data)
