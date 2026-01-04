from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import (
    UserForm,
    PetForm,
    ActivityForm,
    HealthEventForm,
    UserUpdateForm,
    UserSearchForm,
    PetSearchForm,
    ActivitySearchForm,
    HealthEventSearchForm,
    SpeciesSearchForm,
    StatusSearchForm,
    PrioritySearchForm
)

from core.models import (
    Pet,
    Activity,
    HealthEvent,
    Status,
    Priority,
    Species
)

User = get_user_model()


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_users = User.objects.count()
    num_pets = Pet.objects.count()
    num_activities = Activity.objects.count()
    num_health_events = HealthEvent.objects.count()

    context = {
        "num_users": num_users,
        "num_pets": num_pets,
        "num_activities": num_activities,
        "num_health_events": num_health_events,
        "segment": "home"
    }

    return render(request, 'core/index.html', context)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 5
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


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("core:user-list")


class SignUpView(CreateView):
    model = User
    form_class = UserForm
    template_name = "registration/register.html"
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
    paginate_by = 5
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
    paginate_by = 2
    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super(ActivityListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        status = self.request.GET.get("status", "")
        pets = self.request.GET.get("pets", "")
        users = self.request.GET.get("users", "")
        context["search_form"] = ActivitySearchForm(
            initial={
                "title": title,
                "status": status,
                "pets": pets,
                "users": users
            }
        )
        context["segment"] = "activities"
        return context

    def get_queryset(self):
        queryset = Activity.objects.select_related("user", "status", "pet")

        form = ActivitySearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data["title"]:
                queryset = queryset.filter(
                    title__icontains=form.cleaned_data["title"]
                )

            if form.cleaned_data["status"]:
                queryset = queryset.filter(
                    status=form.cleaned_data["status"]
                )

            if form.cleaned_data["pets"]:
                queryset = queryset.filter(
                    pet=form.cleaned_data["pets"]
                )

            if form.cleaned_data["users"]:
                queryset = queryset.filter(
                    user=form.cleaned_data["users"]
                )

        return queryset


class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    def get_object(self, queryset=None):
        try:
            return Activity.objects.select_related("user", "status", "pet").get(pk=self.kwargs["pk"])
        except Activity.DoesNotExist:
            raise Http404("Activity not found")


class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    success_url = reverse_lazy("core:activity-list")


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    success_url = reverse_lazy("core:activity-list")


class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    success_url = reverse_lazy("core:activity-list")


class HealthEventListView(LoginRequiredMixin, ListView):
    model = HealthEvent
    queryset = HealthEvent.objects.all().select_related("priority", "status", "user", "pet")
    paginate_by = 2
    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        status = self.request.GET.get("status", "")
        priority = self.request.GET.get("priority", "")
        pets = self.request.GET.get("pets", "")
        users = self.request.GET.get("users", "")
        context["search_form"] = HealthEventSearchForm(
            initial={
                "title": title,
                "status": status,
                "priority": priority,
                "pets": pets,
                "users": users
            }
        )
        context["segment"] = "health_events"
        return context

    def get_queryset(self):
        queryset = HealthEvent.objects.select_related("priority", "status", "user", "pet")

        form = HealthEventSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data["title"]:
                queryset = queryset.filter(
                    title__icontains=form.cleaned_data["title"]
                )

            if form.cleaned_data["status"]:
                queryset = queryset.filter(
                    status=form.cleaned_data["status"]
                )

            if form.cleaned_data["priority"]:
                queryset = queryset.filter(
                    priority=form.cleaned_data["priority"]
                )

            if form.cleaned_data["pets"]:
                queryset = queryset.filter(
                    pet=form.cleaned_data["pets"]
                )

            if form.cleaned_data["users"]:
                queryset = queryset.filter(
                    user=form.cleaned_data["users"]
                )

        return queryset

class HealthEventDetailView(LoginRequiredMixin, DetailView):
    model = HealthEvent
    def get_object(self, queryset=None):
        try:
            return HealthEvent.objects.select_related("priority", "status", "user", "pet").get(pk=self.kwargs["pk"])
        except HealthEvent.DoesNotExist:
            raise Http404("HealthEvent not found")

class HealthEventCreateView(LoginRequiredMixin, CreateView):
    model = HealthEvent
    form_class = HealthEventForm
    success_url = reverse_lazy("core:healthevent-list")


class HealthEventUpdateView(LoginRequiredMixin, UpdateView):
    model = HealthEvent
    form_class = HealthEventForm
    success_url = reverse_lazy("core:healthevent-list")


class HealthEventDeleteView(LoginRequiredMixin, DeleteView):
    model = HealthEvent
    success_url = reverse_lazy("core:healthevent-list")


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    paginate_by = 5
    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = StatusSearchForm(
            initial={"name": name}
        )
        context["segment"] = "statuses"
        return context

    def get_queryset(self):
        queryset = Status.objects.all()
        form = StatusSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset



class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = "__all__"
    success_url = reverse_lazy("core:status-list")


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    fields = "__all__"
    success_url = reverse_lazy("core:status-list")


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    success_url = reverse_lazy("core:status-list")


class PriorityListView(LoginRequiredMixin, ListView):
    model = Priority
    paginate_by = 5
    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PrioritySearchForm(
            initial={"name": name}
        )
        context["segment"] = "priorities"
        return context
    def get_queryset(self):
        queryset = Priority.objects.all()
        form = PrioritySearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class PriorityCreateView(LoginRequiredMixin, CreateView):
    model = Priority
    fields = "__all__"
    success_url = reverse_lazy("core:priority-list")


class PriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = Priority
    fields = "__all__"
    success_url = reverse_lazy("core:priority-list")


class PriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = Priority
    success_url = reverse_lazy("core:priority-list")


class SpeciesListView(LoginRequiredMixin, ListView):
    model = Species
    paginate_by = 5
    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SpeciesSearchForm(
            initial={"name": name}
        )
        context["segment"] = "species"
        return context
    def get_queryset(self):
        queryset = Species.objects.all()
        form = SpeciesSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset

class SpeciesCreateView(LoginRequiredMixin, CreateView):
    model = Species
    fields = "__all__"
    success_url = reverse_lazy("core:species-list")


class SpeciesUpdateView(LoginRequiredMixin, UpdateView):
    model = Species
    fields = "__all__"
    success_url = reverse_lazy("core:species-list")


class SpeciesDeleteView(LoginRequiredMixin, DeleteView):
    model = Species
    success_url = reverse_lazy("core:species-list")
