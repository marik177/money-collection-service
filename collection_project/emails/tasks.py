from celery import shared_task
from celery.utils.log import get_task_logger

from collection_project.emails.models import Email

logger = get_task_logger(__name__)


def _email_send_failed(self, exc, task_id, args, kwargs, einfo):
    from collection_project.emails.services import email_failed

    email_id = args[0]
    email = Email.objects.get(id=email_id)

    email_failed(email)


@shared_task(bind=True, name="email_send_task", on_failure=_email_send_failed)
def email_send(self, email_id: int) -> Email:
    from collection_project.emails.services import email_send, update_email_status

    email = Email.objects.get(id=email_id)
    update_email_status(email=email, status=Email.Status.SENDING)
    try:
        email = email_send(email=email)
        return email.id

    except Exception as exc:
        logger.warning(f"Exception occurred while sending email: {exc}")
        self.retry(exc=exc, countdown=5)
