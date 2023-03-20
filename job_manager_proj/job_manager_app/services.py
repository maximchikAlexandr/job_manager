from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from django.urls import reverse
from django.utils.safestring import SafeString, mark_safe

from job_manager_app.apps import JobManagerAppConfig
from job_manager_app.models import ServiceAgreement


class ServiceAgreementValidator:
    def __init__(self, agreement: ServiceAgreement) -> None:
        self.__agreement = agreement

    def validate_money(self) -> bool:
        sum_agreement = self.__agreement.amount.amount
        sum_acts = self.__agreement.acts.aggregate(Sum("amount"))["amount__sum"]
        return sum_agreement == sum_acts

    def send_error_message(self, request: WSGIRequest) -> None:
        reverse_url = self.__get_url_for_change_obj()
        message = "Не сходятся деньги в договоре "
        message = message + f'<a href="{reverse_url}"> №{self.__agreement.number}</a>'
        safestr_message: SafeString = mark_safe(message)
        messages.add_message(
            request=request,
            level=messages.ERROR,
            message=safestr_message,
        )

    def __get_url_for_change_obj(self) -> str:
        app_label = JobManagerAppConfig.name
        model_name = self.__agreement.__class__.__name__.lower()
        named_url = f"admin:{app_label}_{model_name}_change"
        return reverse(named_url, args=[self.__agreement.pk])
