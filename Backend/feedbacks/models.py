from datetime import datetime

from django.db import models

from alerts.models import Alert
from cases.models import Case
from feedbacks.utils import FeedbackUtils
from organizations.models import Organization
from users.models import User, Uuid


class FeedbackSet(models.QuerySet):
    @staticmethod
    def get_latest_web_queryset(organization_id):
        if organization_id is None:
            return Feedback.objects.all().order_by("-created_at")[:5]
        else:
            return Feedback.objects.filter(organization=organization_id).order_by("-created_at")[:5]

    @staticmethod
    def get_web_query_set(organization_id, case_id, is_superuser):
        if is_superuser:
            if case_id is not None:
                queryset = Feedback.objects.filter(case=case_id).order_by("id").reverse()
            elif organization_id is not None:
                queryset = Feedback.objects.filter(organization=organization_id).order_by("id").reverse()
            else:
                queryset = Feedback.objects.all().order_by("id").reverse()
        else:
            if case_id is not None:
                queryset = Feedback.objects.filter(case=case_id).order_by("id").reverse()
            else:
                queryset = Feedback.objects.filter(organization=organization_id).order_by("id").reverse()
        return queryset


class Feedback(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="case")
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user", blank=True, null=True)
    uuid = models.ForeignKey(Uuid, on_delete=models.CASCADE, related_name="uuid", blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    is_main = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)
    source = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    current_latitude = models.FloatField(blank=True, null=True)
    current_longitude = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=8000, blank=True, null=True)
    feedback_image = models.ImageField(upload_to=FeedbackUtils.feedback_image_path, blank=True, null=True)

    address = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name="checker")
    checked_on = models.DateTimeField(blank=True, null=True)

    FEEDBACK_STATUSES = (
        ("pending", "Pending"),
        ("relevant", "Relevant"),
        ("irrelevant", "Irrelevant"),
        ("credible", "Credible"),
    )
    feedback_status = models.CharField(max_length=20, choices=FEEDBACK_STATUSES, default="pending")
    is_valid = models.NullBooleanField()

    location_selected_reasons = models.CharField(max_length=5000, blank=True, null=True)
    CHILD_STATUS = (
        ("ok", "Ok"),
        ("dead", "Dead"),
        ("initial", "Initial"),
        ("ill", "Ill"),
        ("wounded", "Wounded"),
    )
    child_status = models.CharField(max_length=20, blank=True, null=True)
    TRANSPORTATION_CHOICES = (
        ("foot", "Foot"),
        ("bus", "Bus"),
        ("car", "Car"),
        ("train", "Train"),
        ("other", "Other"),
    )
    transportation = models.CharField(max_length=20, blank=True, null=True)
    objects = FeedbackSet.as_manager()

    def __str__(self):
        return "Feedback: {id} for case {case}".format(id=self.id, case=self.case)
