from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from core.models import Pet, Activity, HealthEvent, Status, Priority

User = get_user_model()


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class UserSearchForm(forms.Form):
    username = forms.CharField(max_length=150, required=False)


class PetForm(forms.ModelForm):
    owners = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Pet
        fields = "__all__"


class PetSearchForm(forms.Form):
    name = forms.CharField(max_length=150, required=False)


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = "__all__"


class ActivitySearchForm(forms.Form):
    title = forms.CharField(required=False)
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False
    )
    pets = forms.ModelChoiceField(
        queryset=Pet.objects.all(),
        required=False
    )
    users = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False
    )


class HealthEventForm(forms.ModelForm):
    class Meta:
        model = HealthEvent
        fields = "__all__"


class HealthEventSearchForm(forms.Form):
    title = forms.CharField(required=False)
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False
    )
    priority = forms.ModelChoiceField(
        queryset=Priority.objects.all(),
        required=False
    )
    pets = forms.ModelChoiceField(
        queryset=Pet.objects.all(),
        required=False
    )
    users = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False
    )


class SpeciesSearchForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)


class StatusSearchForm(forms.Form):
    name = forms.CharField(max_length=150, required=False)


class PrioritySearchForm(forms.Form):
    name = forms.CharField(max_length=150, required=False)
