from celery import shared_task

from commerce.services import create_service_agreement_file, create_act_file


@shared_task
def create_agreement_task(agreement_id):
    create_service_agreement_file(agreement_id)


@shared_task
def create_act_task(agreement_id):
    create_act_file(agreement_id)
