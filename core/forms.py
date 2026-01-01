from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from django import forms

from core.models import Pet


User = get_user_model()


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")


class PetForm(forms.ModelForm):
    owners = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Pet
        fields = "__all__"