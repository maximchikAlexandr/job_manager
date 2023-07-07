from celery import shared_task
from commerce.services import (
    create_act_file,
    create_crm_deal,
    create_service_agreement_file,
    update_cost_in_crm_deal,
)


@shared_task
def create_agreement_task(agreement_id):
    create_service_agreement_file(agreement_id)


@shared_task
def create_act_task(agreement_id):
    create_act_file(agreement_id)


@shared_task
def create_crm_deal_task(cp_id):
    create_crm_deal(cp_id)


@shared_task
def update_cost_in_crm_deal_task(id_crm_deal, total_cost):
    update_cost_in_crm_deal(id_crm_deal, total_cost)
