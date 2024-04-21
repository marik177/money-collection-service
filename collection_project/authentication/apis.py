from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebTokenView

from collection_project.api.mixins import ApiAuthMixin
from collection_project.authentication.services import auth_logout
from collection_project.users.selectors import user_get_login_data


class UserJwtLoginApi(ObtainJSONWebTokenView):
    pass


class UserJwtLogoutApi(ApiAuthMixin, APIView):
    def post(self, request) -> Response:
        auth_logout(request.user)

        response = Response()

        if settings.JWT_AUTH["JWT_AUTH_COOKIE"] is not None:
            response.delete_cookie(settings.JWT_AUTH["JWT_AUTH_COOKIE"])

        return response


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request) -> Response:
        data = user_get_login_data(user=request.user)

        return Response(data)
