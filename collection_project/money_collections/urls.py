from django.urls import include, path

from collection_project.money_collections.apis.collections import (
    CollectionCreateApi,
    CollectionDeleteApi,
    CollectionDetailApi,
    CollectionListApi,
    CollectionUpdateApi,
)
from collection_project.money_collections.apis.occasions import (
    OccasionCreateApi,
    OccasionDeleteApi,
    OccasionDetailApi,
    OccasionListApi,
    OccasionUpdateApi,
)
from collection_project.money_collections.apis.payments import (
    PaymentCreateApi,
    PaymentDetailApi,
    PaymentListApi,
)

occasions_urlpatterns = [
    path("", OccasionListApi.as_view(), name="list"),
    path("create/", OccasionCreateApi.as_view(), name="create"),
    path("<int:occasion_id>/", OccasionDetailApi.as_view(), name="detail"),
    path("<int:occasion_id>/update/", OccasionUpdateApi.as_view(), name="update"),
    path("<int:occasion_id>/delete/", OccasionDeleteApi.as_view(), name="delete"),
]

collections_urlpatterns = [
    path("", CollectionListApi.as_view(), name="list"),
    path("create/", CollectionCreateApi.as_view(), name="create"),
    path("<int:collection_id>/", CollectionDetailApi.as_view(), name="detail"),
    path("<int:collection_id>/update/", CollectionUpdateApi.as_view(), name="update"),
    path("<int:collection_id>/delete/", CollectionDeleteApi.as_view(), name="delete"),
]

payment_urlpatterns = [
    path("", PaymentListApi.as_view(), name="list"),
    path("create/", PaymentCreateApi.as_view(), name="create"),
    path("<int:payment_id>/", PaymentDetailApi.as_view(), name="detail"),
]

urlpatterns = [
    path("occasions/", include((occasions_urlpatterns, "occasions"))),
    path("collections/", include((collections_urlpatterns, "collections"))),
    path("payments/", include((payment_urlpatterns, "payments"))),
]
