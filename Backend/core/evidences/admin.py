from django.contrib import admin

from core.evidences.models import Evidence


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'case', 'created_at', 'updated_at', 'evidence_image_element']
    list_display_links = ('id', )
