from django.db import transaction

from collection_project.common.services import model_update
from collection_project.money_collections.models import Occasion


def ocassion_create(*, name: str) -> Occasion:
    """Create an occasion"""
    occasion = Occasion.objects.create(name=name)
    return occasion


@transaction.atomic
def occasion_update(*, occasion: Occasion, data) -> Occasion:
    """Update an occasion"""
    fields = ["name"]
    occasion, has_updated = model_update(instance=occasion, fields=fields, data=data)

    return occasion


def occasion_delete(*, occasion: Occasion) -> Occasion:
    """Delete an occasion"""
    occasion.delete()
    return occasion
