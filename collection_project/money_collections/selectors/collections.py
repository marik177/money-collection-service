from collection_project.money_collections.models import Collection


def collections_list():
    return Collection.objects.select_related("author", "occasion").all()


def collection_get(collect_id):
    return Collection.objects.select_related("author", "occasion").get(id=collect_id)
