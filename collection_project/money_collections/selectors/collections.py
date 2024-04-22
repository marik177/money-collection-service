from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from collection_project.money_collections.models import Collection


def collections_list() -> QuerySet[Collection]:
    return Collection.objects.select_related("author", "occasion").all()


def collection_get(collect_id) -> Collection:
    return get_object_or_404(Collection.objects.select_related("author", "occasion"), id=collect_id)
