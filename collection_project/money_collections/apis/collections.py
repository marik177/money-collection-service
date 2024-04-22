from rest_framework import serializers
from rest_framework.views import APIView

from collection_project.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from collection_project.money_collections.models import Collection
from collection_project.money_collections.selectors.collections import collections_list


class CollectionListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Collection
            fields = (
                "id",
                "title",
                "author",
                "occasion",
                "description",
                "planned_amount",
                "cover_image",
                "end_collection_date",
            )

    def get(self, request):
        collections = collections_list()
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=collections,
            request=request,
            view=self,
        )
