from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import UserForm, PetForm, ActivityForm, HealthEventForm, UserUpdateForm, UserSearchForm, PetSearchForm
from core.models import Pet, Activity, HealthEvent


User = get_user_model()


@login_required
def index(request: HttpRequest) -> HttpResponse:
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
        context = super(UserListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = UserSearchForm(
            initial={"username": username}
        )
        context["segment"] = "users"
        return context

    def get_queryset(self):
        queryset = User.objects.all().prefetch_related("pets")
        form = UserSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class UserDetailView(LoginRequiredMixin, DetailView):
    model=User
    def get_object(self, queryset=None):
        if self.request.user.id == self.kwargs.get("pk"):
            return self.request.user
        try:
            return User.objects.prefetch_related("pets").get(pk=self.kwargs["pk"])
        except User.DoesNotExist:
            raise Http404("User not found")

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context["segment"] = "profile"
        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("core:user-list")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("core:user-list")


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("core:user-list")


class PetListView(LoginRequiredMixin, ListView):
    model = Pet
    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super(PetListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PetSearchForm(
            initial={"name": name}
        )
        context["segment"] = "pets"
        return context

    def get_queryset(self):
        queryset = Pet.objects.all().prefetch_related("owners").select_related("species")
        form = PetSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pet
    def get_object(self, queryset=None):
        try:
            return Pet.objects.prefetch_related("owners").select_related("species").get(pk=self.kwargs["pk"])
        except Pet.DoesNotExist:
            raise Http404("Pet not found")

    def get_context_data(self, **kwargs):
        context = super(PetDetailView, self).get_context_data(**kwargs)
        context["segment"] = "profile"
        return context


class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    success_url = reverse_lazy("core:pet-list")


class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    form_class = PetForm
    success_url = reverse_lazy("core:pet-list")


class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    success_url = reverse_lazy("core:pet-list")


@login_required
def toggle_assign_to_pet(request, pk):
    user = User.objects.get(id=request.user.id)
    if (
        Pet.objects.get(id=pk) in user.pets.all()
    ):
        user.pets.remove(pk)
    else:
        user.pets.add(pk)
    return HttpResponseRedirect(reverse_lazy("core:pet-detail", args=[pk]))


class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    queryset = Activity.objects.all().select_related("user", "status", "pet")
    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context["segment"] = "activities"
        return context


class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    success_url = reverse_lazy("core:activity-list")


class HealthEventListView(LoginRequiredMixin, ListView):
    model = HealthEvent
    queryset = HealthEvent.objects.all().select_related("priority", "status", "user", "pet")
    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context["segment"] = "health_events"
        return context

class HealthEventCreateView(LoginRequiredMixin, CreateView):
    model = HealthEvent
    form_class = HealthEventForm
    success_url = reverse_lazy("core:healthevent-list")

