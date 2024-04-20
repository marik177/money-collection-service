from django.urls import include, path

urlpatterns = [
    path("users/", include(("collection_project.users.urls", "users"))),
]
