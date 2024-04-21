from typing import Sequence, Type

from rest_framework.authentication import BaseAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

PermissionClassesType = Sequence[Type[BasePermission]]


class ApiAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        BasicAuthentication,
        SessionAuthentication,
        JSONWebTokenAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated,)
