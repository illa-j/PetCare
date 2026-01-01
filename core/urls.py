from django.urls import path

from .views import (
    index,
    UserListView,
    UserDetailView,
    PetListView,
    ActivityListView,
    HealthEventListView,
    UserCreateView, PetCreateView
)

urlpatterns = [
    path("", index, name="index"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("pets/", PetListView.as_view(), name="pet-list"),
    path("pets/create/", PetCreateView.as_view(), name="pet-create"),
    path("activities/", ActivityListView.as_view(), name="activity-list"),
    path("healthevents/", HealthEventListView.as_view(), name="healthevent-list"),
]

app_name = "core"
