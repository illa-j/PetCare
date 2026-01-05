from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from core.models import Pet, Activity, HealthEvent, Species, Status, Priority


User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    pass

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "species", "breed", "weight", "height", "birth_date")
    search_fields = ["name"]
    list_filter = ["species", "breed", "weight", "height", "birth_date"]

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "scheduled_date", "user", "pet", "status")
    search_fields = ["title", "pet__name"]
    list_filter = ["scheduled_date", "user", "pet", "status"]


@admin.register(HealthEvent)
class HealthEventAdmin(admin.ModelAdmin):
    list_display = ("title", "scheduled_date", "priority", "user", "pet", "status")
    search_fields = ["title", "pet__name", "priority__name"]
    list_filter = ["scheduled_date", "priority", "user", "pet", "status"]

admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Species)
