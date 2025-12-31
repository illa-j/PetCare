from django.urls import path

from .views import (
    index,
    UserListView,
    UserDetailView,
    PetListView,
    ActivityListView,
    HealthEventListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("users/", UserListView.as_view(), name="users"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("pets/", PetListView.as_view(), name="pets"),
    path("activities/", ActivityListView.as_view(), name="activities"),
    path("healthevents/", HealthEventListView.as_view(), name="healthevents"),
]

app_name = "core"
