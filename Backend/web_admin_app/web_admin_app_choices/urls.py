from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'web_admin_app_choices'

urlpatterns = [
    path('school_grades/', SchoolGradesList.as_view(), name='school_grades_list'),
    path('school_grades/<int:pk>/', SchoolGradesDetails.as_view(), name='school_gradesdetails'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
