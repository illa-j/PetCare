from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import (
    Species,
    Pet,
    Priority,
    Status,
    Activity,
    HealthEvent
)

User = get_user_model()

USERNAME = "username"
PASSWORD = "password"


class LoginRequiredTests(TestCase):
    def test_not_auth_user_access(self):
        res = self.client.get(reverse("core:pet-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_auth_user_access(self):
        User.objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.login(username=USERNAME, password=PASSWORD)
        res = self.client.get(reverse("core:pet-list"))
        self.assertEqual(res.status_code, 200)


class UserViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.users = list()
        for i in range(5):
            cls.users.append(
                User.objects.create_user(
                    username=f"{USERNAME}{i}",
                    password=PASSWORD,
                )
            )

    def setUp(self):
        self.users.append(
            User.objects
            .create_user(
                username=USERNAME,
                password=PASSWORD,
            )
        )
        self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )

    def test_list_view_template(self):
        res = self.client.get(reverse("core:user-list"))
        self.assertTemplateUsed(res, "core/user_list.html")

    def test_list_view_paginate(self):
        res = self.client.get(reverse("core:user-list"))
        self.assertTemplateUsed(res, "includes/pagination.html")

    def test_update_view_template(self):
        res = self.client.get(reverse("core:user-update", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "core/user_form.html")

    def test_create_view_template(self):
        res = self.client.get(reverse("core:user-create"))
        self.assertTemplateUsed(res, "core/user_form.html")

    def test_detail_view_template(self):
        res = self.client.get(reverse("core:user-detail", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "core/user_detail.html")

    def test_is_paginated_view_by_five(self):
        res = self.client.get(reverse("core:user-list"))
        self.assertEqual(res.context.get("paginator").per_page, 5)

    def test_users_list_in_list_view(self):
        res = self.client.get(reverse("core:user-list"))
        per_page = res.context["paginator"].per_page
        self.assertEqual(
            self.users[:per_page],
            list(res.context["user_list"])
        )

    def test_user_in_detail_view(self):
        res = self.client.get(reverse("core:user-detail", kwargs={"pk": 1}))
        self.assertIn(
            res.context["user"],
            self.users,
        )

    def test_search_by_name(self):
        res = self.client.get(
            reverse("core:user-list"),
            {"username": f"{USERNAME}0"}
        )
        self.assertContains(res, f"{USERNAME}0")
        self.assertNotContains(res, "username1")

    def test_search_form_in_context(self):
        res = self.client.get(reverse("core:user-list"))
        self.assertIn("search_form", res.context)


class PetViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        species = Species.objects.create(
            name="test"
        )
        cls.pets = list()
        for i in range(5):
            cls.pets.append(
                Pet.objects.create(
                    name=f"test{i}",
                    species=species,
                    breed="test",
                    weight=Decimal("10.3"),
                    height=Decimal("20.5"),
                    birth_date=date(2020, 1, 1),
                )
            )

    def setUp(self):
        User.objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )

    def test_list_view_template(self):
        res = self.client.get(reverse("core:pet-list"))
        self.assertTemplateUsed(res, "core/pet_list.html")

    def test_list_view_paginate(self):
        res = self.client.get(reverse("core:pet-list"))
        self.assertTemplateUsed(res, "includes/pagination.html")

    def test_update_view_template(self):
        res = self.client.get(reverse("core:pet-update", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "core/pet_form.html")

    def test_create_view_template(self):
        res = self.client.get(reverse("core:pet-create"))
        self.assertTemplateUsed(res, "core/pet_form.html")

    def test_detail_view_template(self):
        res = self.client.get(reverse("core:pet-detail", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "core/pet_detail.html")

    def test_is_paginated_view_by_five(self):
        res = self.client.get(reverse("core:pet-list"))
        self.assertEqual(res.context.get("paginator").per_page, 5)

    def test_pets_list_in_list_view(self):
        res = self.client.get(reverse("core:pet-list"))
        per_page = res.context["paginator"].per_page
        self.assertEqual(
            self.pets[:per_page],
            list(res.context["pet_list"])
        )

    def test_pet_in_detail_view(self):
        res = self.client.get(reverse("core:pet-detail", kwargs={"pk": 1}))
        self.assertIn(
            res.context["pet"],
            self.pets,
        )

    def test_search_by_name(self):
        res = self.client.get(
            reverse("core:pet-list"),
            {"name": f"test0"}
        )
        self.assertContains(res, f"test0")
        self.assertNotContains(res, "test1")

    def test_search_form_in_context(self):
        res = self.client.get(reverse("core:pet-list"))
        self.assertIn("search_form", res.context)


class ActivityViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.activities = list()
        user = User.objects.create_user(
            username="test",
            password="test",
        )
        species = Species.objects.create(
            name="test"
        )
        pet = Pet.objects.create(
            name="test",
            species=species,
            breed="test",
            weight=Decimal("10.3"),
            height=Decimal("20.5"),
            birth_date=date(2020, 1, 1),
        )
        status = Status.objects.create(name="test")
        for i in range(5):
            cls.activities.append(
                Activity.objects.create(
                    title=f"test{i}",
                    description="test",
                    scheduled_date=date(2020, 1, 1),
                    status=status,
                    user=user,
                    pet=pet
                )
            )

    def setUp(self):
        User.objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )

    def test_list_view_template(self):
        res = self.client.get(reverse("core:activity-list"))
        self.assertTemplateUsed(res, "core/activity_list.html")

    def test_list_view_paginate(self):
        res = self.client.get(reverse("core:activity-list"))
        self.assertTemplateUsed(res, "includes/pagination.html")

    def test_update_view_template(self):
        res = self.client.get(reverse("core:activity-update", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "core/activity_form.html")

    def test_create_view_template(self):
        res = self.client.get(reverse("core:activity-create"))
        self.assertTemplateUsed(res, "core/activity_form.html")

    def test_detail_view_template(self):
        res = self.client.get(reverse("core:activity-detail", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "core/activity_detail.html")

    def test_is_paginated_view_by_five(self):
        res = self.client.get(reverse("core:activity-list"))
        self.assertEqual(res.context.get("paginator").per_page, 2)

    def test_activities_list_in_list_view(self):
        res = self.client.get(reverse("core:activity-list"))
        per_page = res.context["paginator"].per_page
        self.assertEqual(
            self.activities[:per_page],
            list(res.context["activity_list"])
        )

    def test_activities_in_detail_view(self):
        res = self.client.get(reverse("core:activity-detail", kwargs={"pk": 1}))
        self.assertIn(
            res.context["activity"],
            self.activities,
        )

    def test_search_by_name(self):
        res = self.client.get(
            reverse("core:activity-list"),
            {"title": f"test0"}
        )
        self.assertContains(res, f"test0")
        self.assertNotContains(res, "test1")

    def test_search_form_in_context(self):
        res = self.client.get(reverse("core:activity-list"))
        self.assertIn("search_form", res.context)


class HealthEventsViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.health_events = list()
        user = User.objects.create_user(
            username="test",
            password="test",
        )
        species = Species.objects.create(
            name="test"
        )
        priority = Priority.objects.create(
            name="test"
        )
        status = Status.objects.create(name="test")
        pet = Pet.objects.create(
            name="test",
            species=species,
            breed="test",
            weight=Decimal("10.3"),
            height=Decimal("20.5"),
            birth_date=date(2020, 1, 1),
        )
        for i in range(5):
            cls.health_events.append(
                HealthEvent.objects.create(
                    title=f"test{i}",
                    description="test",
                    scheduled_date=date(2020, 1, 1),
                    status=status,
                    priority=priority,
                    user=user,
                    pet=pet
                )
            )

    def setUp(self):
        User.objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )

    def test_list_view_template(self):
        res = self.client.get(reverse("core:healthevent-list"))
        self.assertTemplateUsed(res, "core/healthevent_list.html")

    def test_list_view_paginate(self):
        res = self.client.get(reverse("core:healthevent-list"))
        self.assertTemplateUsed(res, "includes/pagination.html")

    def test_update_view_template(self):
        res = self.client.get(reverse("core:healthevent-update", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "core/healthevent_form.html")

    def test_create_view_template(self):
        res = self.client.get(reverse("core:healthevent-create"))
        self.assertTemplateUsed(res, "core/healthevent_form.html")

    def test_detail_view_template(self):
        res = self.client.get(reverse("core:healthevent-detail", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "core/healthevent_detail.html")

    def test_is_paginated_view_by_five(self):
        res = self.client.get(reverse("core:healthevent-list"))
        self.assertEqual(res.context.get("paginator").per_page, 2)

    def test_health_events_list_in_list_view(self):
        res = self.client.get(reverse("core:healthevent-list"))
        per_page = res.context["paginator"].per_page
        self.assertEqual(
            self.health_events[:per_page],
            list(res.context["healthevent_list"])
        )

    def test_health_event_in_detail_view(self):
        res = self.client.get(reverse("core:healthevent-detail", kwargs={"pk": 1}))
        self.assertIn(
            res.context["healthevent"],
            self.health_events,
        )

    def test_search_by_name(self):
        res = self.client.get(
            reverse("core:healthevent-list"),
            {"title": f"test0"}
        )
        self.assertContains(res, f"test0")
        self.assertNotContains(res, "test1")

    def test_search_form_in_context(self):
        res = self.client.get(reverse("core:healthevent-list"))
        self.assertIn("search_form", res.context)


class SpeciesViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.species = list()
        for i in range(5):
            cls.species.append(
                Species.objects.create(
                    name=f"test{i}",
                )
            )

    def setUp(self):
        User.objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )

    def test_list_view_template(self):
        res = self.client.get(reverse("core:species-list"))
        self.assertTemplateUsed(res, "core/species_list.html")

    def test_list_view_paginate(self):
        res = self.client.get(reverse("core:species-list"))
        self.assertTemplateUsed(res, "includes/pagination.html")

    def test_update_view_template(self):
        res = self.client.get(reverse("core:species-update", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "core/species_form.html")

    def test_create_view_template(self):
        res = self.client.get(reverse("core:species-create"))
        self.assertTemplateUsed(res, "core/species_form.html")

    def test_is_paginated_view_by_five(self):
        res = self.client.get(reverse("core:species-list"))
        self.assertEqual(res.context.get("paginator").per_page, 5)

    def test_species_list_in_list_view(self):
        res = self.client.get(reverse("core:species-list"))
        per_page = res.context["paginator"].per_page
        self.assertEqual(
            self.species[:per_page],
            list(res.context["species_list"])
        )

    def test_search_by_name(self):
        res = self.client.get(
            reverse("core:species-list"),
            {"name": f"test0"}
        )
        self.assertContains(res, f"test0")
        self.assertNotContains(res, "test1")

    def test_search_form_in_context(self):
        res = self.client.get(reverse("core:species-list"))
        self.assertIn("search_form", res.context)


class PriorityViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.priorities = list()
        for i in range(5):
            cls.priorities.append(
                Priority.objects.create(
                    name=f"test{i}",
                )
            )

    def setUp(self):
        User.objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )

    def test_list_view_template(self):
        res = self.client.get(reverse("core:priority-list"))
        self.assertTemplateUsed(res, "core/priority_list.html")

    def test_list_view_paginate(self):
        res = self.client.get(reverse("core:priority-list"))
        self.assertTemplateUsed(res, "includes/pagination.html")

    def test_update_view_template(self):
        res = self.client.get(reverse("core:priority-update", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "core/priority_form.html")

    def test_create_view_template(self):
        res = self.client.get(reverse("core:priority-create"))
        self.assertTemplateUsed(res, "core/priority_form.html")

    def test_is_paginated_view_by_five(self):
        res = self.client.get(reverse("core:priority-list"))
        self.assertEqual(res.context.get("paginator").per_page, 5)

    def test_species_list_in_list_view(self):
        res = self.client.get(reverse("core:priority-list"))
        per_page = res.context["paginator"].per_page
        self.assertEqual(
            self.priorities[:per_page],
            list(res.context["priority_list"])
        )

    def test_search_by_name(self):
        res = self.client.get(
            reverse("core:priority-list"),
            {"name": f"test0"}
        )
        self.assertContains(res, f"test0")
        self.assertNotContains(res, "test1")

    def test_search_form_in_context(self):
        res = self.client.get(reverse("core:priority-list"))
        self.assertIn("search_form", res.context)


class StatusViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.statuses = list()
        for i in range(5):
            cls.statuses.append(
                Status.objects.create(
                    name=f"test{i}",
                )
            )

    def setUp(self):
        User.objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )

    def test_list_view_template(self):
        res = self.client.get(reverse("core:status-list"))
        self.assertTemplateUsed(res, "core/status_list.html")

    def test_list_view_paginate(self):
        res = self.client.get(reverse("core:status-list"))
        self.assertTemplateUsed(res, "includes/pagination.html")

    def test_update_view_template(self):
        res = self.client.get(reverse("core:status-update", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "core/status_form.html")

    def test_create_view_template(self):
        res = self.client.get(reverse("core:status-create"))
        self.assertTemplateUsed(res, "core/status_form.html")

    def test_is_paginated_view_by_five(self):
        res = self.client.get(reverse("core:status-list"))
        self.assertEqual(res.context.get("paginator").per_page, 5)

    def test_species_list_in_list_view(self):
        res = self.client.get(reverse("core:status-list"))
        per_page = res.context["paginator"].per_page
        self.assertEqual(
            self.statuses[:per_page],
            list(res.context["status_list"])
        )

    def test_search_by_name(self):
        res = self.client.get(
            reverse("core:status-list"),
            {"name": f"test0"}
        )
        self.assertContains(res, f"test0")
        self.assertNotContains(res, "test1")

    def test_search_form_in_context(self):
        res = self.client.get(reverse("core:status-list"))
        self.assertIn("search_form", res.context)
