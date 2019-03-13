import time
import datetime

from django.db import models
from django.db.models import F
from django.utils.safestring import mark_safe
from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from core.alerts.utils import image_path
from core.cases.models import Case


class AlertSet(models.QuerySet):

    def add_distance(self, latitude, longitude):
        return self.annotate(
            distance=Distance('geolocation_point', Point(float(latitude), float(longitude), srid=4326))
        )

    def calc_distance(self, latitude, longitude):
        return self.add_distance(latitude, longitude).filter(distance__lt=F('radius'))

    @staticmethod
    def calc_active():
        now = datetime.datetime.now()
        return Alert.objects.filter(is_active=True, start_timestamp__lt=now, end_timestamp__gt=now)

    def get_mobile_queryset(self, latitude, longitude):
        return self.calc_distance(latitude, longitude).filter(pk__in=Alert.objects.calc_active()).order_by('distance')

    @staticmethod
    def get_web_queryset(active=None, case_id=None):
        if active:
            if case_id is not None:
                return Alert.objects.calc_active().filter(case_id=case_id)
            else:
                return Alert.objects.calc_active()
        else:
            if case_id is not None:
                return Alert.objects.filter(case_id=case_id)
            else:
                return Alert.objects.all()


class Alert(models.Model):

    case_id = models.ForeignKey(Case, on_delete=models.CASCADE)

    geolocation_point = geo_models.PointField(blank=False, null=False)
    radius = models.FloatField(default=5.0)

    ALERT_TYPE_CHOICES = (
        ('amber', 'Amber alert'),
        ('alert', 'Alert'),
    )
    type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES, default='alert')

    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    name = models.CharField(max_length=1024)
    disappearance_date = models.DateTimeField(blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    eye_color = models.CharField(max_length=256, blank=True, null=True)
    hair_color = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    image = models.ImageField(upload_to=image_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AlertSet.as_manager()

    def __str__(self):
        return "Alert for case: {case}".format(case=self.case_id)

    def image_element(self):
        return mark_safe('<img src="http://localhost:8000/media/%s" width="32" height="32" />' % self.image)
