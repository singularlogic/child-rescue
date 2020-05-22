from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path("children/", ChildrenList.as_view(), name="case_list"),
    path("children/<int:pk>/", ChildDetails.as_view(), name="case_details"),
    path("", CaseList.as_view(), name="case_list"),
    path("<int:pk>/", CaseDetails.as_view(), name="case_details"),
    path("social_media/", SocialMediaList.as_view(), name="social_media_list"),
    path("social_media/<int:pk>/", SocialMediaDetails.as_view(), name="social_media_details",),
    path("<int:pk>/volunteers/add/", AddCaseVolunteer.as_view(), name="add_case_volunteers",),
    path("<int:pk>/volunteers/", CaseVolunteerList.as_view(), name="case_volunteers"),
    path("<int:pk>/similar_cases/", SimilarCasesList.as_view(), name="similar_cases_listy",),
    path("<int:pk>/volunteers/<int:volunteer_id>/", CaseVolunteerDetails.as_view(), name="case_volunteers",),
    path("<int:pk>/files/", FileList.as_view(), name="file_list"),
    path("<int:pk>/files/<int:file_id>/", FileDetails.as_view(), name="file_details"),
    path("<int:pk>/files/<int:file_id>/download-image/", DownloadImage.as_view(), name="image_download",),
    path("<int:pk>/files/<int:file_id>/download-file/", DownloadFile.as_view(), name="file_download",),
    path("<int:pk>/feed/", FeedList.as_view(), name="feed_list"),
    path("<int:pk>/feed/<int:feed_id>/", FeedDetails.as_view(), name="feed_details"),
    path("<int:pk>/close_case/", CloseCase.as_view(), name="close_case"),
    path("<int:pk>/archive_case/", ArchiveCase.as_view(), name="archive_case"),
    path("facility_cases/", FacilityCaseList.as_view(), name="facility_case_list"),
    path("facility_cases/<int:pk>/", FacilityCaseDetails.as_view(), name="facility_case_list",),
    path("facility_cases/<int:pk>/state/", FacilityCaseState.as_view(), name="case_state"),
    path("facility_cases/<int:pk>/report_missing/", FacilityCaseReportMissing.as_view(), name="case_state",),
]

urlpatterns = format_suffix_patterns(urlpatterns)
