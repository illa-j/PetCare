from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from core.models import Pet, Activity, HealthEvent


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
    birth_date = forms.DateField()
    class Meta:
        model = Pet
        fields = "__all__"


class PetSearchForm(forms.Form):
    name = forms.CharField(max_length=150, required=False)


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = "__all__"


class HealthEventForm(forms.ModelForm):
    class Meta:
        model = HealthEvent
        fields = "__all__"
