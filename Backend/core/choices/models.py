from django.db import models

from core.organizations.models import Organization


class SchoolGradesManager(models.Manager):

    @staticmethod
    def get_fields_of_organization(organization_id):
        return SchoolGrades.objects.filter(organization_id=organization_id)


class SchoolGrades(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=1024)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SchoolGradesManager()

    def __str__(self):
        return "Organization: {organization} -- {description} -- is_active: {is_active}".format(
            organization=self.organization,
            description=self.description,
            is_active=self.is_active
        )
