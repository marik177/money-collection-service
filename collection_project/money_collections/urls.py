from django.urls import include, path

from collection_project.money_collections.apis.occasions import (
    OccasionCreateApi,
    OccasionDeleteApi,
    OccasionDetailApi,
    OccasionListApi,
    OccasionUpdateApi,
)

occasions_urlpatterns = [
    path("", OccasionListApi.as_view(), name="list"),
    path("create/", OccasionCreateApi.as_view(), name="create"),
    path("<int:occasion_id>/", OccasionDetailApi.as_view(), name="detail"),
    path("<int:occasion_id>/update/", OccasionUpdateApi.as_view(), name="update"),
    path("<int:occasion_id>/delete/", OccasionDeleteApi.as_view(), name="delete"),
]

urlpatterns = [
    path("occasions/", include((occasions_urlpatterns, "occasions"))),
]
