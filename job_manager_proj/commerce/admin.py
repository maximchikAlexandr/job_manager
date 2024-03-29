from urllib.parse import quote

from django.conf import settings
from django.contrib.admin import ModelAdmin, TabularInline, register
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
from commerce.services import (
    create_act_file,
    create_proposal_file,
    create_service_agreement_file,
    create_calculation_file,
)
from commerce.tasks import (
    create_act_task,
    create_agreement_task,
    create_crm_deal_task,
    create_proposal_task,
    create_calculation_task,
)
from shared_mixins import LoggedAdminModelMixin


class PlannedBusinessTripInline(TabularInline):
    model = PlannedBusinessTrip
    extra = 0


@register(BudgetCalculation)
class BudgetCalculationAdmin(ImportExportMixin, LoggedAdminModelMixin, ModelAdmin):
    resource_class = BudgetCalculationResource
    list_display = ("company", "type_of_jobs", "total_cost", "created", "edited")
    readonly_fields = (
        "salary",
        "travel_expenses",
        "transportation_expenses",
        "cost_price",
        "profit",
        "price_excluding_vat",
        "total_cost",
    )
    exclude = (
        "income_taxes",
        "social_security_contributions",
        "depreciation_expenses",
        "accident_insurance",
        "overhead_expenses",
        "vat",
        "calculation_file",
    )
    inlines = (PlannedBusinessTripInline,)
    save_on_top = True
    list_per_page = 15
    search_fields = ("type_of_jobs__name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("commercial_proposal__company", "type_of_jobs").only(
            "commercial_proposal__company__name", "type_of_jobs__name", "total_cost"
        )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save()

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        budget_calculation = BudgetCalculation.objects.get(pk=object_id)

        if budget_calculation.calculation_file:
            encoded_path = quote(budget_calculation.calculation_file)
            url = f"https://disk.yandex.ru/edit/disk{encoded_path}?sk={settings.YANDEX_SK}"
            extra_context["change_calculation_file_url"] = url
        else:
            extra_context["create_calculation_file_url"] = reverse(
                "admin:admin_create_calculation_file", args=(object_id,)
            )
        return super().change_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/create_calculation_file/",
                self.admin_site.admin_view(self.create_calculation_file_view),
                name="admin_create_calculation_file",
            ),
        ]
        return custom_urls + urls

    def create_calculation_file_view(self, request, object_id):
        # create_calculation_file(object_id)
        create_calculation_task.delay(object_id)
        return redirect("https://disk.yandex.ru/client/disk/budget_calculations")

    def company(self, obj):
        try:
            return obj.commercial_proposal.company
        except AttributeError:
            return "Смета не связана с КП"


class BudgetCalculationInline(TabularInline):
    model = BudgetCalculation
    extra = 0
    readonly_fields = ("total_cost",)
    exclude = (
        "salary",
        "income_taxes",
        "social_security_contributions",
        "overhead_expenses",
        "depreciation_expenses",
        "accident_insurance",
        "travel_expenses",
        "transportation_expenses",
        "cost_price",
        "price_excluding_vat",
        "vat",
        "profit",
        "calculation_file",
    )


@register(CommercialProposal)
class CommercialProposalAdmin(ImportExportMixin, LoggedAdminModelMixin, ModelAdmin):
    resource_class = CommercialProposalResource
    inlines = (BudgetCalculationInline,)
    list_display = ("company", "type_of_jobs", "total_cost", "created", "edited")
    readonly_fields = ("total_cost",)
    form = CommercialProposalForm
    save_on_top = True
    list_per_page = 15
    search_fields = ("company__name",)
    exclude = ("crm_deal_id", "proposal_file")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.types_of_jobs_dict = {}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.__get_types_of_jobs_queryset(qs)
        return qs.select_related("company").only("company__name", "total_cost")

    def __get_types_of_jobs_queryset(self, queryset):
        budget_calc_queryset = (
            BudgetCalculation.objects.filter(commercial_proposal__in=queryset)
            .values("commercial_proposal", "type_of_jobs__name")
            .distinct("commercial_proposal", "type_of_jobs__name")
        )

        for it in budget_calc_queryset:
            self.types_of_jobs_dict[it["commercial_proposal"]] = [
                item["type_of_jobs__name"]
                for item in budget_calc_queryset
                if item["commercial_proposal"] == it["commercial_proposal"]
            ]

    def save_model(
        self,
        request: WSGIRequest,
        obj: CommercialProposal,
        form: "CommercialProposalForm",
        change: bool,
    ):
        super().save_model(request, obj, form, change)

        if obj.pk and obj.service_descriptions == "":
            descriptions = list(obj.budget_calculations.select_related("type_of_jobs").values_list(
                "type_of_jobs__service_descriptions", flat=True))
            obj.service_descriptions = "\n\n".join(descriptions)
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

        if proposal.proposal_file:
            encoded_path = quote(proposal.proposal_file)
            url = f"https://disk.yandex.ru/edit/disk{encoded_path}?sk={settings.YANDEX_SK}"
            extra_context["open_proposal_url"] = url
        else:
            extra_context["create_create_proposal_url"] = reverse(
                "admin:admin_create_proposal_file", args=(object_id,)
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
            path(
                "<path:object_id>/create_proposal_file/",
                self.admin_site.admin_view(self.create_proposal_file_view),
                name="admin_create_proposal_file",
            ),
        ]
        return custom_urls + urls

    def create_crm_deal_view(self, request, object_id):
        create_crm_deal_task.delay(object_id)
        return redirect(f"https://{settings.BX24_HOSTNAME}/crm/deal/kanban/category/0/")

    def create_proposal_file_view(self, request, object_id):
        # create_proposal_file(object_id)
        create_proposal_task.delay(object_id)
        return redirect("https://disk.yandex.ru/client/disk/commercial_proposals")

    def type_of_jobs(self, obj):
        return "\n".join(self.types_of_jobs_dict[obj.pk])


class CommercialProposalInline(TabularInline):
    model = CommercialProposal
    extra = 0
    exclude = ("proposal_file",)

    def has_change_permission(self, request, obj=None):
        return False


@register(ServiceAgreement)
class ServiceAgreementJobAdmin(ImportExportMixin, LoggedAdminModelMixin, ModelAdmin):
    resource_class = ServiceAgreementResource
    inlines = (CommercialProposalInline,)
    list_display = ("number", "company", "amount", "created", "edited")
    readonly_fields = ("amount",)
    form = ServiceAgreementForm
    save_on_top = True
    list_per_page = 15
    ordering = ("-date_of_signing",)
    exclude = ("task_id", "agreement_file", "act_file")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.companies_dict = {}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.__get_companies_queryset(qs)
        return qs.only("number", "amount")

    def __get_companies_queryset(self, queryset):
        budget_calc_queryset = (
            CommercialProposal.objects.filter(service_agreement__in=queryset)
            .values("service_agreement", "company__name")
            .distinct("service_agreement", "company__name")
        )

        for it in budget_calc_queryset:
            self.companies_dict[it["service_agreement"]] = [
                item["company__name"]
                for item in budget_calc_queryset
                if item["service_agreement"] == it["service_agreement"]
            ]

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
        # create_service_agreement_file(object_id)
        return redirect("https://disk.yandex.ru/client/disk/agreements")

    def create_act_file_view(self, request, object_id):
        create_act_task.delay(object_id)
        # create_act_file(object_id)
        return redirect("https://disk.yandex.ru/client/disk/acts")

    def company(self, obj):
        try:
            return self.companies_dict[obj.pk]
        except (AttributeError, KeyError):
            return "Договор не связан с КП"
