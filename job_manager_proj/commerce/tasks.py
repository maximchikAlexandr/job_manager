from celery import shared_task

from job_manager_proj.celery import app
from commerce.services import (
    create_act_file,
    create_calculation_file,
    create_crm_deal,
    create_proposal_file,
    create_service_agreement_file,
    update_cost_in_crm_deal,
    check_deal_stage
)


@shared_task
def create_agreement_task(agreement_id):
    create_service_agreement_file(agreement_id)


@shared_task
def create_act_task(agreement_id):
    create_act_file(agreement_id)


@shared_task
def create_proposal_task(proposal_id):
    create_proposal_file(proposal_id)

@shared_task
def create_calculation_task(calculation_id):
    create_calculation_file(calculation_id)

@shared_task
def create_crm_deal_task(cp_id):
    create_crm_deal(cp_id)


@shared_task
def update_cost_in_crm_deal_task(id_crm_deal, total_cost):
    update_cost_in_crm_deal(id_crm_deal, total_cost)


@app.task
def check_deal_stage_task():
    check_deal_stage()
