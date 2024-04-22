import sys
from datetime import datetime, timedelta

from django.db import transaction

from collection_project.common.services import model_update
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
    end_collection_date: datetime = datetime.utcnow() + timedelta(days=7),
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
    return collection


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
