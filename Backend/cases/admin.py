from django.contrib import admin

from .models import *


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Child._meta.fields]
    list_display_links = ("id",)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Case._meta.fields]
    list_display_links = ("id",)


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SocialMedia._meta.fields]


@admin.register(FacilityHistory)
class FacilityHistoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FacilityHistory._meta.fields]
    list_display_links = ("id",)


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Follower._meta.fields]
    list_display_links = ("id",)


@admin.register(CaseVolunteer)
class CaseVolunteerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CaseVolunteer._meta.fields]
    list_display_links = ("id",)


@admin.register(CaseVolunteerLocation)
class CaseVolunteerLocationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CaseVolunteerLocation._meta.fields]
    list_display_links = ("id",)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in File._meta.fields]
    list_display_links = ("id",)


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Feed._meta.fields]
    list_display_links = ("id",)


@admin.register(AnonymizedCase)
class AnonymizedCaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AnonymizedCase._meta.fields]
    list_display_links = ("id",)


@admin.register(SharedCase)
class SharedCaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SharedCase._meta.fields]
    list_display_links = ("id",)


@admin.register(LinkedCase)
class LinkedCaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LinkedCase._meta.fields]
    list_display_links = ("id",)
