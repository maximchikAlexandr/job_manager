from django.urls import include, path

from management import views

urlpatterns = [
    path('month-job/departments/', views.DepartmentInMonthJobAPIView.as_view()),
    path('month-job/years/', views.YearInMonthJobListAPIView.as_view()),
    path('month-job/', views.MonthJobListAPIView.as_view()),

    path('salary/departments/', views.DepartmentSalaryJobAPIView.as_view()),
    path('salary/years/', views.YearInSalaryListAPIView.as_view()),
    path('salary/months/', views.MonthInSalaryListAPIView.as_view()),
    path('salary/', views.SalaryListAPIView.as_view()),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
