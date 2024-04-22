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
from collection_project.users.models import BaseUser
from collection_project.users.selectors import get_user, user_get_login_data, user_list
from collection_project.users.services import user_create, user_update


class UserListApi(ApiAuthMixin, APIView):
    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        email = serializers.EmailField(required=False)

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("id", "email")

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request) -> Response:
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
            view=self,
        )


class UserCreateApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("email", "password", "first_name", "last_name")

    def post(self, request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_create(**serializer.validated_data)
        cache.clear()
        return Response(status=status.HTTP_201_CREATED)


class UserDetailApi(ApiAuthMixin, APIView):
    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, user_id) -> Response:
        user = get_user(user_id=user_id)
        return Response(user_get_login_data(user=user))


class UserUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        password = serializers.CharField(required=False)

    def post(self, request, user_id) -> Response:
        user = get_user(user_id=user_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_update(user=user, data=serializer.validated_data)
        cache.clear()
        return Response(status=status.HTTP_200_OK)
