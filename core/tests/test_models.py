from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import (
    Species,
    Pet,
    Activity,
    Priority,
    Status,
    HealthEvent
)


User = get_user_model()


class SpeciesTests(TestCase):
    def test_species_verbose_name(self):
        self.assertEqual(Species._meta.verbose_name, "Species")

    def test_species_verbose_name_plural(self):
        self.assertEqual(Species._meta.verbose_name_plural, "Species")

    def test_species_str(self):
        species = Species.objects.create(
            name="test"
        )
        self.assertEqual(str(species), "test")

    def test_species_name_max_length(self):
        self.assertEqual(Species._meta.get_field("name").max_length, 200)


class PetTests(TestCase):
    def test_pet_name_max_length(self):
        self.assertEqual(Pet._meta.get_field("name").max_length, 150)

    def test_pet_breed_max_length(self):
        self.assertEqual(Pet._meta.get_field("breed").max_length, 200)

    def test_pet_str(self):
        pet = Pet.objects.create(
            name="test",
            species=Species.objects.create(
                name="test"
            ),
            breed="test",
            weight=Decimal("10.3"),
            height=Decimal("20.5"),
            birth_date=date(2020, 1, 1),
        )
        self.assertEqual(str(pet), f"{pet.name} (species: {pet.species})")

    def test_pet_weight_max_value_validation(self):
        with self.assertRaises(ValidationError):
            Pet.objects.create(
                name="test",
                species=Species.objects.create(
                    name="test"
                ),
                breed="test",
                weight=Decimal("1000.38"),
                height=Decimal("20.5"),
                birth_date=date(2020, 1, 1),
            ).full_clean()

    def test_pet_height_max_value_validation(self):
        with self.assertRaises(ValidationError):
            Pet.objects.create(
                name="test",
                species=Species.objects.create(
                    name="test"
                ),
                breed="test",
                weight=Decimal("10.38"),
                height=Decimal("1000.5"),
                birth_date=date(2020, 1, 1),
            ).full_clean()

    def test_pet_weight_min_value_validation(self):
        with self.assertRaises(ValidationError):
            Pet.objects.create(
                name="test",
                species=Species.objects.create(
                    name="test"
                ),
                breed="test",
                weight=Decimal("-1"),
                height=Decimal("20.5"),
                birth_date=date(2020, 1, 1),
            ).full_clean()

    def test_pet_height_min_value_validation(self):
        with self.assertRaises(ValidationError):
            Pet.objects.create(
                name="test",
                species=Species.objects.create(
                    name="test"
                ),
                breed="test",
                weight=Decimal("10.38"),
                height=Decimal("-1"),
                birth_date=date(2020, 1, 1),
            ).full_clean()


class StatusTests(TestCase):
    def test_status_verbose_name(self):
        self.assertEqual(Status._meta.verbose_name, "Status")

    def test_status_verbose_name_plural(self):
        self.assertEqual(Status._meta.verbose_name_plural, "Statuses")

    def test_status_name_max_length(self):
        self.assertEqual(Status._meta.get_field("name").max_length, 150)

    def test_status_str(self):
        status = Status.objects.create(
            name="test"
        )
        self.assertEqual(str(status), "test")


class ActivityTests(TestCase):
    def test_activity_verbose_name(self):
        self.assertEqual(Activity._meta.verbose_name, "Activity")

    def test_activity_verbose_name_plural(self):
        self.assertEqual(Activity._meta.verbose_name_plural, "Activities")

    def test_activity_ordering(self):
        self.assertEqual(Activity._meta.ordering, ["scheduled_date"])

    def test_activity_str(self):
        activity = Activity.objects.create(
            title="test",
            description="test",
            scheduled_date=date(2020, 1, 1),
            status=Status.objects.create(name="test"),
            user=User.objects.create_user(
                username="test",
                password="test",
            ),
            pet=Pet.objects.create(
                name="test",
                species=Species.objects.create(
                    name="test"
                ),
                breed="test",
                weight=Decimal("10.3"),
                height=Decimal("20.5"),
                birth_date=date(2020, 1, 1),
            )
        )
        self.assertEqual(str(activity), f"{activity.title} (date: {activity.scheduled_date})")

    def test_activity_title_max_length(self):
        self.assertEqual(Activity._meta.get_field("title").max_length, 150)

    def test_activity_description_max_length(self):
        with self.assertRaises(ValidationError):
            Activity.objects.create(
                title="test",
                description="".join("1" for i in range(501)),
                scheduled_date=date(2020, 1, 1),
                status=Status.objects.create(name="test"),
                user=User.objects.create_user(
                    username="test",
                    password="test",
                ),
                pet=Pet.objects.create(
                    name="test",
                    species=Species.objects.create(
                        name="test"
                    ),
                    breed="test",
                    weight=Decimal("10.3"),
                    height=Decimal("20.5"),
                    birth_date=date(2020, 1, 1),
                )
            ).full_clean()


class PriorityTests(TestCase):
    def test_priority_verbose_name(self):
        self.assertEqual(Priority._meta.verbose_name, "Priority")
    def test_priority_verbose_name_plural(self):
        self.assertEqual(Priority._meta.verbose_name_plural, "Priorities")
    def test_priority_name_max_length(self):
        self.assertEqual(Priority._meta.get_field("name").max_length, 150)
    def test_priority_str(self):
        priority = Priority.objects.create(
            name="test",
        )
        self.assertEqual(str(priority), f"{priority.name}")


class HealthEventTests(TestCase):
    def test_health_event_verbose_name(self):
        self.assertEqual(HealthEvent._meta.verbose_name, "Health_Event")

    def test_health_event_verbose_name_plural(self):
        self.assertEqual(HealthEvent._meta.verbose_name_plural, "Health_Events")

    def test_health_event_ordering(self):
        self.assertEqual(HealthEvent._meta.ordering, ["scheduled_date"])

    def test_health_event_str(self):
        health_event = HealthEvent.objects.create(
            title="test",
            description="test",
            scheduled_date=date(2020, 1, 1),
            user=User.objects.create_user(
                username="test",
                password="test",
            ),
            status=Status.objects.create(
                name="test"
            ),
            priority=Priority.objects.create(
                name="test",
            ),
            pet=Pet.objects.create(
                name="test",
                species=Species.objects.create(
                    name="test"
                ),
                breed="test",
                weight=Decimal("10.3"),
                height=Decimal("20.5"),
                birth_date=date(2020, 1, 1),
            )
        )
        self.assertEqual(str(health_event), f"{health_event.title} (date: {health_event.scheduled_date})")

    def test_health_event_title_max_length(self):
        self.assertEqual(HealthEvent._meta.get_field("title").max_length, 150)

    def test_health_event_description_max_length(self):
        with self.assertRaises(ValidationError):
            HealthEvent.objects.create(
                title="test",
                description="".join("1" for i in range(501)),
                scheduled_date=date(2020, 1, 1),
                user=User.objects.create_user(
                    username="test",
                    password="test",
                ),
                status=Status.objects.create(
                    name="test"
                ),
                priority=Priority.objects.create(
                    name="test",
                ),
                pet=Pet.objects.create(
                    name="test",
                    species=Species.objects.create(
                        name="test"
                    ),
                    breed="test",
                    weight=Decimal("10.3"),
                    height=Decimal("20.5"),
                    birth_date=date(2020, 1, 1),
                )
            ).full_clean()
