import sys
from datetime import datetime, timedelta

from collection_project.core.exceptions import ApplicationError
from collection_project.money_collections.models import (
    Collection,
    Occasion,
)
from collection_project.users.models import BaseUser


def collection_create(
    *,
    title: str,
    author: str,
    occasion: int,
    description: str,
    planned_amount: int = sys.maxsize,
    cover_image: str,
    end_collection_date: datetime = datetime.utcnow() + timedelta(days=7),
) -> Collection:
    """Create a collection"""
    occasion, created = Occasion.objects.get_or_create(name=occasion)
    try:
        author = BaseUser.objects.get(email=author)
    except BaseUser.DoesNotExist:
        raise ApplicationError(f"Author with email {author} does not exist")
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
