from django.contrib import admin

from .models import FCMDevice


@admin.register(FCMDevice)
class FCMDeviceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FCMDevice._meta.fields]
    list_display_links = ("id",)
