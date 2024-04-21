from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from collection_project.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from collection_project.money_collections.models import Occasion
from collection_project.money_collections.selectors.occasions import get_occasion, get_occasions
from collection_project.money_collections.services.occasion import ocassion_create, occasion_delete, occasion_update


class OccasionListApi(APIView):
    """List all occasions"""

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Occasion
            fields = (
                "id",
                "name",
            )

    def get(self, request) -> Response:
        occasions = get_occasions()
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=occasions,
            request=request,
            view=self,
        )


class OccasionCreateApi(APIView):
    """Create an occasion"""

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Occasion
            fields = ("name",)

    def post(self, request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ocassion_create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class OccasionDetailApi(APIView):
    """Retrieve an occasion"""

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Occasion
            fields = (
                "id",
                "name",
            )

    def get(self, request, occasion_id) -> Response:
        occasion = get_occasion(occasion_id=occasion_id)
        serializer = self.OutputSerializer(occasion)
        return Response(serializer.data)


class OccasionUpdateApi(APIView):
    """Update an occasion"""

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Occasion
            fields = ("name",)

    def put(self, request, occasion_id) -> Response:
        occasion = get_occasion(occasion_id=occasion_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        occasion_update(occasion=occasion, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class OccasionDeleteApi(APIView):
    """Delete an occasion"""

    def delete(self, request, occasion_id) -> Response:
        occasion = get_occasion(occasion_id=occasion_id)
        occasion_delete(occasion=occasion)
        return Response(status=status.HTTP_204_NO_CONTENT)
