from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from collection_project.money_collections.models import Occasion


def get_occasion(*, occasion_id: int) -> Occasion:
    return get_object_or_404(Occasion, id=occasion_id)


def get_occasions() -> QuerySet[Occasion]:
    return Occasion.objects.all().order_by("-created_at")
