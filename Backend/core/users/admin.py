from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['profile_image_element', 'id', 'email', 'organization', 'role', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_end_user']
    list_display_links = ('id', 'email')


@admin.register(Uuid)
class UuidAdmin(admin.ModelAdmin):
    pass


@admin.register(UuidActivity)
class UuidActivityAdmin(admin.ModelAdmin):
    pass

