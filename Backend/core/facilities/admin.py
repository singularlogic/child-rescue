from django.contrib import admin

from .models import *


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Facility._meta.fields]
    list_display_links = ('id',)


