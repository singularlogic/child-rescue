from django.contrib import admin

from .models import *


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Child._meta.fields]
    list_display_links = ('id',)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Case._meta.fields]
    list_display_links = ('id', )


@admin.register(DemographicData)
class DemographicDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DemographicData._meta.fields]


@admin.register(MedicalData)
class MedicalDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MedicalData._meta.fields]


@admin.register(SocialData)
class SocialDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SocialData._meta.fields]


@admin.register(PhysicalData)
class PhysicalDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PhysicalData._meta.fields]


@admin.register(ProfileData)
class ProfileDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProfileData._meta.fields]
