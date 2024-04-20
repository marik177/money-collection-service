from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from collection_project.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from collection_project.users.models import BaseUser
from collection_project.users.services import user_create, user_list


# TODO: When JWT is resolved, add authenticated version
class UserListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("id", "email", "is_admin")

    def get(self, request):
        users = user_list()
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
            fields = ("email",)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)
