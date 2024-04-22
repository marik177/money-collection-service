from django.utils.datetime_safe import datetime

from collection_project.money_collections.models import (
    Collection,
    Payment,
)
from collection_project.users.models import BaseUser


def get_contributor_full_name_or_email(*, payment: Payment) -> str:
    first_name = payment.contributor.first_name
    last_name = payment.contributor.last_name
    if first_name and last_name:
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

    return payment
