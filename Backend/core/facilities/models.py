from django.db import models
from core.organizations.models import Organization

from django.contrib.gis.db import models as geo_models


class Facility(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    supports_hosting = models.BooleanField(default=True)

    email = models.EmailField(blank=True, null=True)

    phone = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)

    address = models.CharField(max_length=250, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    geolocation_point = geo_models.PointField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    capacity = models.IntegerField()

    class Meta:
        db_table = 'facility'
        verbose_name_plural = 'facilities'

    def __str__(self):
        return self.name

    def get_full_address(self):
        return self.address + ' ' + self.city + ' ' + self.postal_code + ' ' + self.country

