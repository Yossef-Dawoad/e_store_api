from celery import shared_task

from . import mail


@shared_task
def send_invoice_email_task(email: str):  # noqa: ANN201
    return mail.send_order_invoice_email(email)
