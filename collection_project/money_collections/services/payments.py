from django.utils.datetime_safe import datetime

from collection_project.emails.models import Email
from collection_project.emails.tasks import email_send as email_send_task
from collection_project.money_collections.models import (
    Collection,
    Payment,
)
from collection_project.users.models import BaseUser


def get_contributor_full_name_or_email(*, payment: Payment) -> str:
    """Get full name or email of contributor"""
    first_name = payment.contributor.first_name
    last_name = payment.contributor.last_name
    if first_name or last_name:
        return f"{first_name} {last_name}"
    return payment.contributor.email


def payment_create(
    *,
    collection_id: int,
    email: str,
    amount: int,
    first_name: str = "",
    last_name: str = "",
    payment_date: datetime = datetime.utcnow(),
) -> Payment:
    """Create a payment"""
    collection = Collection.objects.get(id=collection_id)
    try:
        contributor = BaseUser.objects.get(email=email)
    except BaseUser.DoesNotExist:
        contributor = BaseUser.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
    payment = Payment.objects.create(
        collection=collection,
        contributor=contributor,
        amount=amount,
        payment_date=payment_date,
    )
    email: Email = create_email_payment_template(user=contributor, payment=payment)

    # Send email in background on creation payment
    email_send_task.delay(email.id)

    return payment


def create_email_payment_template(user: BaseUser, payment: Payment) -> Email:
    """Create email template for payment"""
    email = Email.objects.create(
        to=user.email,
        subject=f"Оплата '{payment.collection.title}'",
        html=f"Оплата '{payment.amount}' была произведена",
        plain_text=f"Оплата '{payment.amount}' была произведена",
    )
    return email
