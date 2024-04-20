from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from collection_project.users.models import BaseUser
from collection_project.users.services import user_list


# TODO: When JWT is resolved, add authenticated version
class UserListApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("id", "email", "is_admin")

    def get(self, request):
        users = user_list()

        data = self.OutputSerializer(users, many=True).data

        return Response(data)
