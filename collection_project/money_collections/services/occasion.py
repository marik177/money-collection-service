# from django.db import transaction
#
# from collection_project.common.services import model_update
from collection_project.money_collections.models import Occasion


def ocassion_create(*, name: str) -> Occasion:
    occasion = Occasion.objects.create(name=name)
    return occasion
