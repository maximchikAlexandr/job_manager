from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Department
from django.db.models import Q
from management.models import MonthJob
from management.serializers import (
    DepartmentSerializer,
    MonthJobSerializer,
    YearSerializer,
    MonthInSalarySerializer,
    SalarySerializer,
)


# Report "MonthJob"
class DepartmentInMonthJobAPIView(ListAPIView):
    queryset = Department.objects.filter(employees__jobs__isnull=False).distinct()
    serializer_class = DepartmentSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        responses={200: DepartmentSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        """
        Get a list of all departments for which job is planned or produced.
        """
        return super().get(request, *args, **kwargs)


class YearInMonthJobListAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id_departament": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=["id_departament"],
        ),
        responses={200: YearSerializer(many=True)},
    )
    def post(self, request):
        """
        Get a list of years in which work is planned for the department with a specific 'id_departament'.
        """
        id_departament = request.data["id_departament"]
        queryset = (
            MonthJob.objects.filter(employee__department__id=id_departament)
            .values("month__year")
            .distinct()
        )
        serializer = YearSerializer(queryset, many=True)
        return Response(serializer.data)


class MonthJobListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id_departament": openapi.Schema(type=openapi.TYPE_INTEGER),
                "year": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=["id_departament", "year"],
        ),
        responses={200: MonthJobSerializer(many=True)},
    )
    def post(self, request):
        """
        Get a report on the department's workload in the year 'year'.
        """
        year = request.data["year"]
        id_departament = request.data["id_departament"]
        queryset = MonthJob.objects.filter(
            Q(month__year=year) & Q(employee__department__id=id_departament)
        ).order_by("month__start_date")
        serializer = MonthJobSerializer(queryset, many=True)
        return Response(serializer.data)


# Report "Salary"
class DepartmentSalaryJobAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Department.objects.filter(
        Q(employees__jobs__isnull=False) & Q(employees__jobs__status="produced")
    ).distinct()
    serializer_class = DepartmentSerializer

    @swagger_auto_schema(
        responses={200: DepartmentSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        """
        Get a list of all departments for which job is produced.
        """
        return super().get(request, *args, **kwargs)


class YearInSalaryListAPIView(APIView):
    permissions_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id_departament": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=["id_departament"],
        ),
        responses={200: YearSerializer(many=True)},
    )
    def post(self, request):
        """
        Get a list of years in which work is produced for the department with a specific 'id_departament'.
        """
        id_departament = request.data["id_departament"]
        queryset = (
            MonthJob.objects.filter(
                Q(employee__department__id=id_departament) & Q(status="produced")
            )
            .values("month__year")
            .distinct()
        )
        serializer = YearSerializer(queryset, many=True)
        return Response(serializer.data)


class MonthInSalaryListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id_departament": openapi.Schema(type=openapi.TYPE_INTEGER),
                "year": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=["id_departament", "year"],
        ),
        responses={200: MonthInSalarySerializer(many=True)},
    )
    def post(self, request):
        """
        Get a list of months in which work is produced for the department with a specific
        'id_departament'.
        """
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
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id_departament": openapi.Schema(type=openapi.TYPE_INTEGER),
                "year": openapi.Schema(type=openapi.TYPE_INTEGER),
                "number_month": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=["id_departament", "year", "number_month"],
        ),
        responses={200: SalarySerializer(many=True)},
    )
    def post(self, request):
        """
        Get a report on the department's salary
        """
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
