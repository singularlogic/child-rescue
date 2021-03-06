"""Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("auth/", include("rest_framework_social_oauth2.urls")),
    path("api/v1/users/", include("users.urls", namespace="users_v1")),
    path(
        "api/v1/organizations/",
        include("organizations.urls", namespace="organizations_v1"),
    ),
    path("api/v1/cases/", include("cases.urls", namespace="cases_v1")),
    path("api/v1/alerts/", include("alerts.urls", namespace="alerts_v1")),
    path("api/v1/feedbacks/", include("feedbacks.urls", namespace="feedbacks_v1")),
    path("api/v1/analytics/", include("analytics.urls", namespace="analytics_v1")),
    path("api/v1/facilities/", include("facilities.urls", namespace="facilities_v1")),
    path("api/v1/places/", include("places.urls", namespace="places_v1")),
    path("api/v1/firebase/", include("firebase.urls", namespace="firebase_v1")),
    # path('web_admin/api/v1/users/', include('web_admin_app.web_admin_app_users.urls', namespace='web_admin_users_v1')),
    # path('web_admin/api/v1/organizations/', include('web_admin_app.web_admin_app_organizations.urls', namespace='web_admin_organizations_v1')),
    # path('web_admin/api/v1/cases/', include('web_admin_app.web_admin_app_cases.urls', namespace='web_admin_cases_v1')),
    # path('web_admin/api/v1/alerts/', include('web_admin_app.web_admin_app_alerts.urls', namespace='web_admin_alerts_v1')),
    # path('web_admin/api/v1/facilities/', include('web_admin_app.web_admin_app_facilities.urls', namespace='web_admin_facilities_v1')),
    # path('web_admin/api/v1/feedbacks/', include('web_admin_app.web_admin_app_feedbacks.urls', namespace='web_admin_feedbacks_v1')),
    # path('mobile/api/v1/users/', include('mobile_app.mobile_app_users.urls', namespace='mobile_users_v1')),
    # path('mobile/api/v1/cases/', include('mobile_app.mobile_app_cases.urls', namespace='mobile_cases_v1')),
    # path('mobile/api/v1/alerts/', include('mobile_app.mobile_app_alerts.urls', namespace='mobile_alerts_v1')),
    # path('mobile/api/v1/feedbacks/', include('mobile_app.mobile_app_feedbacks.urls', namespace='mobile_feedbacks_v1')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
