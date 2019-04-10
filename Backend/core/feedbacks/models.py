from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from core.cases.models import Case
from core.feedbacks.utils import feedback_image_path
from core.users.models import User
from core.alerts.models import Alert
from core.cases.utils import CaseUtils


class ImageUpload(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=CaseUtils.image_upload_path, blank=True, null=True)


class Feedback(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case')
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user')

    source = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    current_latitude = models.FloatField(blank=True, null=True)
    current_longitude = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=8000, blank=True, null=True)
    feedback_image = models.CharField(max_length=254, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='checker')
    checked_on = models.DateTimeField(blank=True, null=True)

    FEEDBACK_STATUSES = (
        ('pending', 'Pending'),
        ('relevant', 'Relevant'),
        ('irrelevant', 'Irrelevant'),
        ('credible', 'Credible'),
    )
    feedback_status = models.CharField(max_length=20, choices=FEEDBACK_STATUSES, default='pending')
    is_valid = models.NullBooleanField()

    location_selected_reasons = models.CharField(max_length=5000, blank=True, null=True)
    CHILD_STATUS = (
        ('ok', 'Ok'),
        ('dead', 'Dead'),
        ('initial', 'Initial'),
        ('ill', 'Ill'),
        ('wounded', 'Wounded'),
    )
    child_status = models.CharField(max_length=20, choices=CHILD_STATUS, blank=True, null=True)
    TRANSPORTATION_CHOICES = (
        ('foot', 'Foot'),
        ('bus', 'Bus'),
        ('car', 'Car'),
        ('train', 'Train'),
        ('other', 'Other'),
    )
    transportation = models.CharField(max_length=20, choices=TRANSPORTATION_CHOICES, blank=True, null=True)

    def __str__(self):
        return "Feedback: {id} for case {case}".format(id=self.id, case=self.case)
