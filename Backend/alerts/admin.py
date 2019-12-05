from django.contrib import admin

from alerts.models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    # list_display = ['id', 'case', 'created_at', 'updated_at', 'evidence_image_element']
    # list_display_links = ('id', )
    pass
