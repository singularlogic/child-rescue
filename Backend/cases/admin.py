from django.contrib import admin

from .models import *


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'disappearance_date', 'found_date', 'conditions_of_disappearance', 'reasons_of_disappearance', 'child_state', 'has_mobile_phone', 'has_money_or_credit', 'has_area_knowledge']
    list_display_links = ('id', )
