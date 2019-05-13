from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'web_admin_app_facilities'

urlpatterns = [
    path('', FacilityList.as_view(), name='facility_list'),
    path('<int:pk>/', FacilityDetail.as_view(), name='facility_details'),
    path('<int:pk>/completeness/', FacilityCompleteness.as_view(), name='facility_completeness'),
    path('<int:pk>/add_child_in_facility/', FacilityAddChild.as_view(), name='add_child_in_facility'),
    path('<int:pk>/remove_child_from_facility/', FacilityRemoveChild.as_view(), name='remove_child_from_facility'),
    path('<int:pk>/facility_assign_hfm/', FacilityAssignHFM.as_view(), name='facility_assign_hfm'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
