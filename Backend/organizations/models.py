from django.db import models

from organizations.utils import OrganizationUtils
from django.utils.safestring import mark_safe


class OrganizationSet(models.QuerySet):
    @staticmethod
    def get_organization_users(organization_id, user_id=None, role=None):
        from users.models import User

        list_of_roles = [
            "organization_manager",
            "coordinator",
            "case_manager",
            "network_manager",
            "facility_manager",
            "volunteer",
        ]
        if role is not None:
            list_of_roles = [role]
        if user_id is not None:
            result = User.objects.filter(id=user_id, organization_id=organization_id, role__in=list_of_roles)
        else:
            result = User.objects.filter(organization_id=organization_id, role__in=list_of_roles)
        return result

    @staticmethod
    def get_organization_facilities(organization_id):
        from facilities.models import Facility

        a = Facility.objects.filter(organization_id=organization_id).values()
        return a


class Organization(models.Model):
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    facebook = models.CharField(max_length=128, blank=True, null=True)
    instagram = models.CharField(max_length=128, blank=True, null=True)
    twitter = models.CharField(max_length=128, blank=True, null=True)
    how_to_become_volunteer = models.CharField(max_length=4056, blank=True, null=True)
    missing_child_actions = models.CharField(max_length=4056, blank=True, null=True)
    description = models.CharField(max_length=4056, blank=True, null=True)
    logo = models.ImageField(upload_to=OrganizationUtils.logo_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrganizationSet.as_manager()

    class Meta:
        db_table = "organization"
        verbose_name_plural = "organizations"

    def __str__(self):
        return "ID: {}".format(self.id)

    def profile_image_element(self):
        return mark_safe('<img src="http://localhost:8000/media/%s" width="16" height="16" />' % self.logo)
