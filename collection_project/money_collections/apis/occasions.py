from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from collection_project.api.mixins import ApiAuthMixin
from collection_project.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from collection_project.common.permissions import IsAdmin
from collection_project.money_collections.models import Occasion
from collection_project.money_collections.selectors.occasions import get_occasion, get_occasions
from collection_project.money_collections.services.occasion import (
    ocassion_create,
    occasion_delete,
    occasion_update,
)


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

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers("Authorization"))
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
        cache.clear()
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

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, occasion_id) -> Response:
        occasion = get_occasion(occasion_id=occasion_id)
        serializer = self.OutputSerializer(occasion)
        return Response(serializer.data)


class OccasionUpdateApi(ApiAuthMixin, APIView):
    """Update an occasion"""

    permission_classes = [IsAdmin]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Occasion
            fields = ("name",)

    def put(self, request, occasion_id) -> Response:
        occasion = get_occasion(occasion_id=occasion_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        occasion_update(occasion=occasion, data=serializer.validated_data)
        cache.clear()
        return Response(status=status.HTTP_200_OK)


class OccasionDeleteApi(ApiAuthMixin, APIView):
    """Delete an occasion"""

    permission_classes = [IsAdmin]

    def delete(self, request, occasion_id) -> Response:
        occasion = get_occasion(occasion_id=occasion_id)
        occasion_delete(occasion=occasion)
        cache.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
