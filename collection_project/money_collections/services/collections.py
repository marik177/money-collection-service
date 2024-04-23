import sys
from datetime import datetime, timedelta

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from collection_project.common.services import model_update
from collection_project.emails.models import Email
from collection_project.emails.tasks import email_send as email_send_task
from collection_project.money_collections.models import (
    Collection,
    Occasion,
)
from collection_project.users.models import BaseUser


def collection_create(
    *,
    title: str,
    author: BaseUser,
    occasion: int,
    description: str,
    planned_amount: int = sys.maxsize,
    cover_image: str,
    end_collection_date: datetime = timezone.now() + timedelta(days=7),
) -> Collection:
    """Create a collection"""
    occasion, created = Occasion.objects.get_or_create(name=occasion)
    collection = Collection.objects.create(
        title=title,
        author=author,
        occasion=occasion,
        description=description,
        planned_amount=planned_amount,
        cover_image=cover_image,
        end_collection_date=end_collection_date,
    )

    email: Email = create_email_collection_template(user=author, collection=collection)

    # Send email in background on creation collection
    email_send_task.delay(email.id)

    return collection


def create_email_collection_template(user: BaseUser, collection: Collection) -> Email:
    """Create email template for collection"""
    email = Email.objects.create(
        to=user.email,
        subject=f"Сбор денег' {collection.title}' создан",
        html=f"Сбор денег, организованный вами '{collection.description}' был создан",
        plain_text=f"Сбор денег, организованный вами '{collection.description}' был создан",
    )
    return email


@transaction.atomic
def collection_update(*, collection: Collection, data) -> Collection:
    """Update a collection"""
    fields = ["title", "description", "planned_amount", "cover_image", "end_collection_date"]
    collection, has_updated = model_update(instance=collection, fields=fields, data=data)

    return collection


def collection_delete(*, collection: Collection) -> Collection:
    """Delete a collection"""
    collection.delete()
    return collection


def get_contributors_number(collection: Collection) -> int:
    return len(set(collection.payments.values_list("contributor_id", flat=True)))


def get_collected_amount(collection: Collection) -> int:
    return collection.payments.aggregate(full_amount=Sum("amount"))["full_amount"] or 0
