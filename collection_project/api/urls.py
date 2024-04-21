from django.urls import include, path

urlpatterns = [
    path("users/", include(("collection_project.users.urls", "users"))),
    path("auth/", include(("collection_project.authentication.urls", "authentication"))),
]
