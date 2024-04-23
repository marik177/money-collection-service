from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.utils import timezone

from collection_project.common.services import model_update
from collection_project.core.exceptions import ApplicationError
from collection_project.emails.models import Email


@transaction.atomic
def email_failed(email: Email) -> Email:
    """Mark an email as failed"""
    if email.status != Email.Status.SENDING:
        raise ApplicationError(f"Cannot mark as failed non-sending emails. Current status is {email.status}")

    email, has_updated = model_update(instance=email, fields=["status"], data={"status": Email.Status.FAILED})
    return email


@transaction.atomic
def email_send(email: Email) -> Email:
    """Send an email"""
    if email.status != Email.Status.SENDING:
        raise ApplicationError(f"Cannot send non-ready to send emails. Current status is {email.status}")

    subject = email.subject
    from_email = settings.DEFAULT_FROM_EMAIL
    to = email.to

    html = email.html
    plain_text = email.plain_text

    msg = EmailMultiAlternatives(subject, plain_text, from_email, [to])
    msg.attach_alternative(html, "text/html")

    msg.send()

    email, has_updated = model_update(
        instance=email, fields=["status", "sent_at"], data={"status": Email.Status.SENT, "sent_at": timezone.now()}
    )
    return email


@transaction.atomic
def update_email_status(email: Email, status: str) -> Email:
    """Update an email status"""
    email, has_updated = model_update(instance=email, fields=["status"], data={"status": status})
    return email
