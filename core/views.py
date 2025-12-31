from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView

from core.models import Pet, Activity, HealthEvent


User = get_user_model()


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""
    num_users = User.objects.count()
    num_pets = Pet.objects.count()
    num_planned_activities = Activity.objects.filter(status__name="Pending").count()
    num_planned_health_events = HealthEvent.objects.filter(status__name="Pending").count()

    context = {
        "num_users": num_users,
        "num_pets": num_pets,
        "num_planned_activities": num_planned_activities,
        "num_planned_health_events": num_planned_health_events,
        "segment": "home"
    }

    return render(request, 'core/index.html', context)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context["segment"] = "users"
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context["segment"] = "profile"
        return context
