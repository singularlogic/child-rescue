from django.contrib import admin

from core.choices.models import SchoolGrades


@admin.register(SchoolGrades)
class SchoolGradesAdmin(admin.ModelAdmin):
    # list_display = ['id', 'case', 'created_at', 'updated_at', 'evidence_image_element']
    # list_display_links = ('id', )
    pass
