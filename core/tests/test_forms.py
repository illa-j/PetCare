from datetime import date
from decimal import Decimal

from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from core.forms import (
    UserForm,
    UserUpdateForm,
    UserSearchForm,
    PetForm,
    PetSearchForm,
    ActivitySearchForm,
    HealthEventSearchForm,
    SpeciesSearchForm,
    StatusSearchForm,
    PrioritySearchForm
)
from core.models import Species

User = get_user_model()


class UserFormTests(TestCase):
    def test_form_contains_first_name_field(self):
        form = UserForm()
        self.assertIn("first_name", form.fields)

    def test_form_contains_last_name_field(self):
        form = UserForm()
        self.assertIn("last_name", form.fields)

    def test_form_contains_email_field(self):
        form = UserForm()
        self.assertIn("email", form.fields)


class UserUpdateFormTests(TestCase):
    def test_form_contains_only_necessary_fields(self):
        form = UserUpdateForm()
        self.assertListEqual(list(form.fields), ["username", "first_name", "last_name", "email"])


class UserSearchFormTests(TestCase):
    def test_form_contains_username_field(self):
        form = UserSearchForm()
        self.assertIn("username", form.fields)


class PetFormTests(TestCase):
    def test_pet_creation(self):
        form = PetForm({
            "name": "test",
            "species": Species.objects.create(
                name="test"
            ).id,
            "breed": "test",
            "weight": Decimal("10.38"),
            "height": Decimal("10.34"),
            "birth_date": date(2020, 1, 1),
            "owners": [
                User.objects.create_user(
                    username="user",
                    password="password",
                ).id
            ]
        })
        self.assertTrue(form.is_valid())

    def test_form_contains_owners_field(self):
        form = PetForm()
        self.assertIsInstance(
            form.fields["owners"].widget,
            forms.CheckboxSelectMultiple
        )


class PetSearchFormTests(TestCase):
    def test_form_contains_name_field(self):
        form = PetSearchForm()
        self.assertIn("name", form.fields)


class ActivitySearchFormTests(TestCase):
    def test_form_contains_title_field(self):
        form = ActivitySearchForm()
        self.assertIn("title", form.fields)

    def test_form_contains_status_field(self):
        form = ActivitySearchForm()
        self.assertIn("status", form.fields)
        self.assertIsInstance(
            form.fields["status"],
            forms.ModelChoiceField
        )

    def test_form_contains_pets_field(self):
        form = ActivitySearchForm()
        self.assertIsInstance(
            form.fields["pets"],
            forms.ModelChoiceField
        )

    def test_form_contains_users_field(self):
        form = ActivitySearchForm()
        self.assertIsInstance(
            form.fields["users"],
            forms.ModelChoiceField
        )


class HealthEventSearchFormTests(TestCase):
    def test_form_contains_title_field(self):
        form = HealthEventSearchForm()
        self.assertIn("title", form.fields)

    def test_form_contains_status_field(self):
        form = HealthEventSearchForm()
        self.assertIn("status", form.fields)
        self.assertIsInstance(
            form.fields["status"],
            forms.ModelChoiceField
        )

    def test_form_contains_priority_field(self):
        form = HealthEventSearchForm()
        self.assertIn("priority", form.fields)
        self.assertIsInstance(
            form.fields["priority"],
            forms.ModelChoiceField
        )

    def test_form_contains_pets_field(self):
        form = HealthEventSearchForm()
        self.assertIn("pets", form.fields)
        self.assertIsInstance(
            form.fields["pets"],
            forms.ModelChoiceField
        )

    def test_form_contains_users_field(self):
        form = HealthEventSearchForm()
        self.assertIn("users", form.fields)
        self.assertIsInstance(
            form.fields["users"],
            forms.ModelChoiceField
        )


class SpeciesSearchFormTests(TestCase):
    def test_form_name_title_field(self):
        form = SpeciesSearchForm()
        self.assertIn("name", form.fields)


class StatusSearchFormTests(TestCase):
    def test_form_name_title_field(self):
        form = StatusSearchForm()
        self.assertIn("name", form.fields)


class PrioritySearchFormTests(TestCase):
    def test_form_name_title_field(self):
        form = PrioritySearchForm()
        self.assertIn("name", form.fields)
