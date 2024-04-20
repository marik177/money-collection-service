from django.urls import path

from .apis import UserCreateApi, UserListApi

urlpatterns = [
    path("", UserListApi.as_view(), name="list"),
    path("create/", UserCreateApi.as_view(), name="create"),
]
