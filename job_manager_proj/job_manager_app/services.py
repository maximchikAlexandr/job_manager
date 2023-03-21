from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from django.urls import reverse
from django.utils.safestring import SafeString, mark_safe

from job_manager_app.apps import JobManagerAppConfig
from job_manager_app.models import ServiceAgreement


class BaseValidator:
    NAME_FIELD: str = ""
    TEXT_BEFORE_LINK: str = ""
    TEXT_AFTER_LINK: str = ""
    NAME_SUBOBJECTS: str = ""

    def __init__(self, obj) -> None:
        self.__obj = obj

    def has_valid_sum(self) -> bool:
        sum_obj = getattr(self.__obj, self.NAME_FIELD)
        subobjects = getattr(self.__obj, self.NAME_SUBOBJECTS)
        sum_subobjects = subobjects.aggregate(Sum(self.NAME_FIELD))
        sum_subobjects = sum_subobjects[f"{self.NAME_FIELD}__sum"]
        return sum_obj == sum_subobjects

    def send_error_message(self, request: WSGIRequest) -> None:
        reverse_url = self.__get_url_for_change_obj()
        message = (
                self.TEXT_BEFORE_LINK
                + f'<a href="{reverse_url}">{str(self.__obj)}</a>'
                + self.TEXT_AFTER_LINK
        )
        safestr_message: SafeString = mark_safe(message)
        messages.add_message(
            request=request,
            level=messages.ERROR,
            message=safestr_message,
        )

    def __get_url_for_change_obj(self) -> str:
        app_label = JobManagerAppConfig.name
        model_name = self.__obj.__class__.__name__.lower()
        named_url = f"admin:{app_label}_{model_name}_change"
        return reverse(named_url, args=[self.__obj.pk])


class ServiceAgreementValidator(BaseValidator):
    NAME_FIELD: str = "amount"
    TEXT_BEFORE_LINK: str = "Не сходятся деньги в договоре "
    NAME_SUBOBJECTS: str = "acts"


class ActOfCompletedWorkValidator(BaseValidator):
    NAME_FIELD: str = "man_hours"
    TEXT_BEFORE_LINK: str = "Не сходятся человеко-часы в акте "
    NAME_SUBOBJECTS: str = "jobs"
