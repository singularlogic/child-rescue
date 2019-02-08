from django.contrib import admin

from .models import *


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass
