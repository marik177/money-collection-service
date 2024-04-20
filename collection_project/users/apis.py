from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from collection_project.users.models import BaseUser
from collection_project.users.services import user_create, user_list


# TODO: When JWT is resolved, add authenticated version
class UserListApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("id", "email", "is_admin")

    def get(self, request):
        users = user_list()
        data = self.OutputSerializer(users, many=True).data
        print(request.query_params, "request.query_params")
        return Response(data)


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
