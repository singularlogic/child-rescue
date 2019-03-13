from django.db import models
from django.utils.safestring import mark_safe

from core.cases.models import Case
from core.evidences.utils import evidence_image_path
from core.users.models import User


class Evidence(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    current_latitude = models.FloatField(blank=True, null=True)
    current_longitude = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=8000)
    evidence_image = models.ImageField(upload_to=evidence_image_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Evidence for case {case}".format(case=self.case)

    def evidence_image_element(self):
        return mark_safe('<img src="http://localhost:8000/media/%s" width="32" height="32" />' % self.evidence_image)
