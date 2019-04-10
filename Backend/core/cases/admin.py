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


@admin.register(PsychologicalData)
class PsychologicalDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PsychologicalData._meta.fields]


@admin.register(PhysicalData)
class PhysicalDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PhysicalData._meta.fields]


@admin.register(PersonalData)
class PersonalDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PersonalData._meta.fields]


@admin.register(SocialMediaData)
class SocialMediaDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SocialMediaData._meta.fields]


@admin.register(FacilityHistory)
class FacilityHistoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FacilityHistory._meta.fields]
    list_display_links = ('id',)

