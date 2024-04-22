from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from collection_project.api.mixins import (
    ApiAuthMixin,
)
from collection_project.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from collection_project.common.permissions import IsAdmin, IsAuthor
from collection_project.money_collections.models import Collection
from collection_project.money_collections.selectors.collections import (
    collection_get,
    collections_list,
)
from collection_project.money_collections.services.collections import (
    collection_create,
    collection_delete,
    collection_update,
    get_collected_amount,
    get_contributors_number,
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
        contributors = serializers.SerializerMethodField()
        collected_amount = serializers.SerializerMethodField()

        class Meta:
            model = Collection
            fields = (
                "id",
                "title",
                "author",
                "occasion",
                "description",
                "planned_amount",
                "collected_amount",
                "contributors",
                "cover_image",
                "end_collection_date",
            )

        def get_contributors(self, obj: Collection) -> int:
            return get_contributors_number(collection=obj)

        def get_collected_amount(self, obj: Collection) -> int:
            return get_collected_amount(collection=obj)

    def get(self, request, collection_id) -> Response:
        collection = collection_get(collection_id)
        serializer = self.OutputSerializer(collection)
        return Response(serializer.data)


class CollectionCreateApi(ApiAuthMixin, APIView):
    """Create a collection"""

    class InputSerializer(serializers.ModelSerializer):
        occasion = serializers.CharField()

        class Meta:
            model = Collection
            fields = (
                "title",
                "occasion",
                "description",
                "planned_amount",
                "cover_image",
                "end_collection_date",
            )

    def post(self, request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = request.user
        collection_create(author=author, **serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class CollectionUpdateApi(ApiAuthMixin, APIView):
    """Update a collection"""

    permission_classes = [IsAuthor]

    class InputSerializer(serializers.ModelSerializer):
        occasion = serializers.CharField()

        class Meta:
            model = Collection
            fields = (
                "title",
                "occasion",
                "description",
                "planned_amount",
                "cover_image",
                "end_collection_date",
            )

    def put(self, request, collection_id) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection = collection_get(collection_id)
        self.check_object_permissions(request, collection)
        collection_update(collection=collection, data=serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class CollectionDeleteApi(ApiAuthMixin, APIView):
    """Delete a collection"""

    permission_classes = [IsAdmin]

    def delete(self, request, collection_id) -> Response:
        collection = collection_get(collection_id)
        collection_delete(collection=collection)
        return Response(status=status.HTTP_204_NO_CONTENT)
