import datetime

from rest_framework import status
from rest_framework.response import Response

from django.db import models
from django.db.models import F
from django.utils.safestring import mark_safe
from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from tzlocal import get_localzone

from core.cases.models import Case


class AlertSet(models.QuerySet):

    def add_distance(self, latitude, longitude):
        return self.annotate(
            distance=Distance('geolocation_point', Point(float(latitude), float(longitude), srid=4326))
        )

    def calc_distance(self, latitude, longitude):
        return self.add_distance(latitude, longitude).filter(distance__lte=F('radius'))

    @staticmethod
    def calc_active():
        local_now = datetime.datetime.now(get_localzone())
        return Alert.objects.filter(is_active=True, start__lt=local_now, end__gt=local_now)

    def get_mobile_queryset(self, latitude, longitude):
        return self.calc_distance(latitude, longitude).filter(pk__in=Alert.objects.calc_active()).order_by('distance')

    @staticmethod
    def get_web_queryset(active=None, case_id=None):
        if active:
            if case_id is not None:
                return Alert.objects.calc_active().filter(case=case_id)
            else:
                return Alert.objects.calc_active()
        else:
            if case_id is not None:
                return Alert.objects.filter(case=case_id)
            else:
                return Alert.objects.all()

    @staticmethod
    def deactivate(alert_id):

        if alert_id is None:
            return Response('We should pass a valid id', status=status.HTTP_404_NOT_FOUND)

        alert = Alert.objects.get(pk=alert_id)
        if not alert.is_active:
            return Response('Alert was already inactive', status=status.HTTP_200_OK)

        alert.is_active = False
        alert.save()
        return Response('Alert was deactivated', status=status.HTTP_200_OK)


class Alert(models.Model):

    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    geolocation_point = geo_models.PointField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
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

