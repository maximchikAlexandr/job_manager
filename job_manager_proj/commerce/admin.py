from urllib.parse import quote

from django.conf import settings
from django.contrib.admin import TabularInline, register
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.urls import path, reverse
from import_export.admin import ImportExportMixin

from commerce.forms import CommercialProposalForm, ServiceAgreementForm
from commerce.models import (
    BudgetCalculation,
    CommercialProposal,
    PlannedBusinessTrip,
    ServiceAgreement,
)
from commerce.resources import (
    BudgetCalculationResource,
    CommercialProposalResource,
    ServiceAgreementResource,
)
from commerce.services import check_deal_stage
from commerce.tasks import create_act_task, create_agreement_task, create_crm_deal_task
from shared_classes import AbstractModelAdmin


class PlannedBusinessTripInline(TabularInline):
    model = PlannedBusinessTrip
    extra = 0


@register(BudgetCalculation)
class BudgetCalculationAdmin(ImportExportMixin, AbstractModelAdmin):
    resource_class = BudgetCalculationResource
    list_display = ("company", "type_of_jobs", "total_cost", "created", "edited")
    readonly_fields = ("total_cost",)
    inlines = (PlannedBusinessTripInline,)
    save_on_top = True
    list_per_page = 15
    search_fields = ("type_of_jobs__name",)

    def company(self, obj):
        try:
            return obj.commercial_proposal.company
        except AttributeError:
            return "Смета не связана с КП"


class BudgetCalculationInline(TabularInline):
    model = BudgetCalculation
    extra = 0
    readonly_fields = ("total_cost",)


@register(CommercialProposal)
class CommercialProposalAdmin(ImportExportMixin, AbstractModelAdmin):
    resource_class = CommercialProposalResource
    inlines = (BudgetCalculationInline,)
    list_display = ("company", "type_of_jobs", "total_cost", "created", "edited")
    readonly_fields = ("total_cost",)
    form = CommercialProposalForm
    save_on_top = True
    list_per_page = 15
    search_fields = ("company__name",)
    exclude = ("crm_deal_id",)

    def type_of_jobs(self, obj):
        queryset = obj.budget_calculations.all()
        types = set(str(calc.type_of_jobs) for calc in queryset)
        return "\n".join(types)

    def save_model(
        self,
        request: WSGIRequest,
        obj: CommercialProposal,
        form: "CommercialProposalForm",
        change: bool,
    ):
        super().save_model(request, obj, form, change)

        if obj.pk and obj.service_descriptions == "":
            queryset = obj.budget_calculations.all()
            for calc in queryset:
                obj.service_descriptions += (
                    f"{calc.type_of_jobs.service_descriptions}\n\n"
                )
            super().save_model(request, obj, form, change)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        proposal = CommercialProposal.objects.get(pk=object_id)

        if proposal.crm_deal_id:
            url = f"https://{settings.BX24_HOSTNAME}/crm/deal/details/{proposal.crm_deal_id}/"
            extra_context["open_deal_url"] = url
        else:
            extra_context["create_deal_url"] = reverse(
                "admin:admin_create_crm_deal", args=(object_id,)
            )

        return super().change_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/create_crm_deal/",
                self.admin_site.admin_view(self.create_crm_deal_view),
                name="admin_create_crm_deal",
            ),
        ]
        return custom_urls + urls

    def create_crm_deal_view(self, request, object_id):
        create_crm_deal_task.delay(object_id)
        return redirect(f"https://{settings.BX24_HOSTNAME}/crm/deal/kanban/category/0/")


class CommercialProposalInline(TabularInline):
    model = CommercialProposal
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


@register(ServiceAgreement)
class ServiceAgreementJobAdmin(ImportExportMixin, AbstractModelAdmin):
    resource_class = ServiceAgreementResource
    inlines = (CommercialProposalInline,)
    list_display = ("number", "company", "amount", "created", "edited")
    readonly_fields = ("amount",)
    form = ServiceAgreementForm
    save_on_top = True
    list_per_page = 15
    ordering = ("-date_of_signing",)
    exclude = ("task_id", "agreement_file", "act_file")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        agreement = ServiceAgreement.objects.get(pk=object_id)

        if agreement.agreement_file:
            encoded_path = quote(agreement.agreement_file)
            url = f"https://disk.yandex.ru/edit/disk{encoded_path}?sk={settings.YANDEX_SK}"
            extra_context["change_agreement_file_url"] = url
            if agreement.act_file:
                encoded_path = quote(agreement.act_file)
                url = f"https://disk.yandex.ru/edit/disk{encoded_path}?sk={settings.YANDEX_SK}"
                extra_context["change_act_file_url"] = url
            else:
                extra_context["create_act_file_url"] = reverse(
                    "admin:admin_create_act", args=(object_id,)
                )
        else:
            extra_context["create_agreement_file_url"] = reverse(
                "admin:admin_create_agreement", args=(object_id,)
            )
        check_deal_stage()
        return super().change_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/create_agreement_file/",
                self.admin_site.admin_view(self.create_agreement_file_view),
                name="admin_create_agreement",
            ),
            path(
                "<path:object_id>/create_act_file/",
                self.admin_site.admin_view(self.create_act_file_view),
                name="admin_create_act",
            ),
        ]
        return custom_urls + urls

    def create_agreement_file_view(self, request, object_id):
        create_agreement_task.delay(object_id)
        return redirect(f"https://disk.yandex.ru/client/disk/agreements")

    def create_act_file_view(self, request, object_id):
        create_act_task.delay(object_id)
        return redirect(f"https://disk.yandex.ru/client/disk/acts")

    def company(self, obj):
        try:
            proposal = obj.commercial_proposals.first()
            return str(proposal.company)
        except AttributeError:
            return "Договор не связан с КП"
