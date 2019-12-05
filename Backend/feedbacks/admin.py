from django.contrib import admin

from feedbacks.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["id", "case", "created_at", "updated_at"]
    list_display_links = ("id",)
