from django.db import models

from django.contrib.gis.db import models as geo_models

from organizations.models import Organization


class FacilitySet(models.QuerySet):
    @staticmethod
    def get_web_queryset(organization_id=None, is_hosting=None):
        queryset = Facility.objects.all()
        if organization_id is not None:
            queryset = queryset.filter(organization_id=organization_id)
        if is_hosting:
            queryset = queryset.filter(supports_hosting=True)
        return queryset.order_by("id").reverse()

    @staticmethod
    def add_child_to_facility(facility_id, child_id, date_entered):
        from cases.models import Case, FacilityHistory

        case = Case.objects.get(child_id=child_id)
        case.presence_status = "present"
        case.status = "inactive"
        case.arrival_at_facility_date = date_entered
        case.save()
        FacilityHistory.objects.create(
            facility=Facility.objects.get(pk=facility_id), case=case, date_entered=date_entered, is_active=True,
        )

    @staticmethod
    def remove_child_from_facility(facility_id, child_id, date_left):
        from cases.models import Case, FacilityHistory

        facility_history_object = FacilityHistory.objects.filter(
            case_id=child_id, facility_id=facility_id, is_active=True
        ).first()
        facility_history_object.date_left = date_left
        facility_history_object.is_active = False
        facility_history_object.save()

        case = Case.objects.get(child_id=child_id)
        case.presence_status = ""
        case.status = "inactive"
        case.save()


class Facility(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    supports_hosting = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    capacity = models.IntegerField(blank=True, null=True)
    objects = FacilitySet.as_manager()

    class Meta:
        db_table = "facility"
        # unique_together = ('organization', 'name',)
        verbose_name_plural = "facilities"

    def __str__(self):
        return self.name

    def get_full_address(self):
        return self.address + " " + self.city + " " + self.postal_code + " " + self.country
