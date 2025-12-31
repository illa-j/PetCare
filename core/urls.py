from django.urls import path

from .views import (
    index,
    UserListView,
    UserDetailView,
)


urlpatterns = [
    path("", index, name="index"),
    path("users/", UserListView.as_view(), name="users"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
]

app_name = "core"
