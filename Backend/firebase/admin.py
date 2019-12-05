from django.contrib import admin

from .models import FCMDevice


@admin.register(FCMDevice)
class FCMDeviceAdmin(admin.ModelAdmin):
    pass
