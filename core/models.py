from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

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

