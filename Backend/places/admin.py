from django.contrib import admin

from .models import *


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Place._meta.fields]
    list_display_links = ("id",)

