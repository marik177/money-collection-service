from collection_project.money_collections.models import Occasion


def get_occasions():
    return Occasion.objects.all().order_by("-created_at")
