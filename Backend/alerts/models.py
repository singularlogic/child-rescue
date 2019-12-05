import datetime

import toolz
from rest_framework import status
from rest_framework.response import Response

from django.db import models
from django.db.models import F
from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from tzlocal import get_localzone

from cases.models import Case
from organizations.models import Organization


class AlertSet(models.QuerySet):
    def add_distance(self, latitude, longitude):
        return self.annotate(
            distance=Distance("geolocation_point", Point(float(latitude), float(longitude), srid=4326))
        )

    def calc_distance(self, latitude, longitude):
        return self.add_distance(latitude, longitude).filter(distance__lte=F("radius") * 1000)

    @staticmethod
    def calc_active():
        local_now = datetime.datetime.now(get_localzone())
        return Alert.objects.filter(is_active=True, start__lt=local_now, end__gt=local_now)

    @staticmethod
    def mark_active():
        local_now = datetime.datetime.now(get_localzone())
        alerts_to_fix = Alert.objects.filter(is_active=True, end__lt=local_now)
        for alert in alerts_to_fix:
            alert.is_active = False
            alert.save()

    def get_mobile_queryset(self, latitude, longitude):
        result = self.calc_distance(latitude, longitude).filter(pk__in=Alert.objects.calc_active()).order_by("distance")
        return toolz.unique(result, key=lambda x: x.case)

    def get_latest_web_queryset(self, organization_id):
        self.mark_active()
        return Alert.objects.filter(organization=organization_id).order_by("-start")[:5]

    def get_web_queryset(self, active=None, case_id=None, organization_id=None):
        self.mark_active()
        queryset = Alert.objects.all()
        if active is not None:
            active = True if active == "true" else False
            queryset = queryset.filter(is_active=active)
        if case_id is not None:
            queryset = queryset.filter(case=case_id)
        elif organization_id is not None:
            queryset = queryset.filter(organization=organization_id)
        return queryset.order_by("id").reverse()

    @staticmethod
    def deactivate(alert_id):
        if alert_id is None:
            return Response("We should pass a valid id", status=status.HTTP_404_NOT_FOUND)

        alert = Alert.objects.get(pk=alert_id)
        if not alert.is_active:
            return Response("Alert was already inactive", status=status.HTTP_200_OK)

        alert.is_active = False
        alert.end = datetime.datetime.now()
        alert.save()
        return Response("Alert was deactivated", status=status.HTTP_200_OK)


class Alert(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    geolocation_point = geo_models.PointField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    custom_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    radius = models.FloatField(default=5.0)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AlertSet.as_manager()

    def __str__(self):
        return "Alert: {id} for case: {case}".format(id=self.id, case=self.case)
