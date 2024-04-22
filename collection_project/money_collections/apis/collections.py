from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from collection_project.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from collection_project.money_collections.models import Collection
from collection_project.money_collections.selectors.collections import (
    collection_get,
    collections_list,
)
from collection_project.money_collections.services.collections import (
    collection_create,
)


class CollectionListApi(APIView):
    """List all collections"""

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class OutputSerializer(serializers.ModelSerializer):
        occasion = serializers.ReadOnlyField(source="occasion.name")

        class Meta:
            model = Collection
            fields = (
                "title",
                "occasion",
                "description",
                "end_collection_date",
            )

    def get(self, request) -> Response:
        collections = collections_list()
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=collections,
            request=request,
            view=self,
        )


class CollectionDetailApi(APIView):
    """Retrieve a collection"""

    class OutputSerializer(serializers.ModelSerializer):
        author = serializers.ReadOnlyField(source="author.email")
        occasion = serializers.ReadOnlyField(source="occasion.name")

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

    def get(self, request, collection_id) -> Response:
        collection = collection_get(collection_id)
        serializer = self.OutputSerializer(collection)
        return Response(serializer.data)


class CollectionCreateApi(APIView):
    """Create a collection"""

    class InputSerializer(serializers.ModelSerializer):
        author = serializers.EmailField()
        occasion = serializers.CharField()

        class Meta:
            model = Collection
            fields = (
                "title",
                "author",
                "occasion",
                "description",
                "planned_amount",
                "cover_image",
                "end_collection_date",
            )

    def post(self, request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection_create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)
