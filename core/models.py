from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator


class User(AbstractUser):
    pass


class Species(models.Model):
    name = models.CharField(max_length=200)


class Pet(models.Model):
    owners = models.ManyToManyField(
        User,
        related_name="pets"
    )
    name = models.CharField(max_length=150, unique=True)
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="pets"
    )
    breed = models.CharField(max_length=200)
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    birth_date = models.DateField()


class Status(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Activity(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(
        blank=True,
        validators=[MaxLengthValidator(500)]
    )
    scheduled_date = models.DateField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="activities"
    )
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="activities"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="activities"
    )

    class Meta:
        ordering = ["scheduled_date"]

class Priority(models.Model):
    name = models.CharField(max_length=150, unique=True)

class HealthEvent(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(
        blank=True,
        validators=[MaxLengthValidator(500)]
    )
    scheduled_date = models.DateField()
    priority = models.ForeignKey(
        Priority,
        on_delete=models.PROTECT,
        related_name="health_events"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="health_events"
    )
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="health_events"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="health_events"
    )

    class Meta:
        ordering = ["scheduled_date"]