from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from collection_project.users.filters import BaseUserFilter
from collection_project.users.models import BaseUser


def get_user(*, user_id: int) -> BaseUser:
    return get_object_or_404(BaseUser, id=user_id)


def user_get_login_data(*, user: BaseUser) -> dict[str, Any]:
    return {
        "id": user.id,
        "email": user.email,
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


def user_list(*, filters: dict | None = None) -> QuerySet[BaseUser]:
    filters = filters or {}
    qs = BaseUser.objects.all()
    return BaseUserFilter(filters, queryset=qs).qs
