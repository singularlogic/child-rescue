from django.contrib.postgres.fields import JSONField
from django.db import models

from cases.models import Case
from feedbacks.models import Feedback
from users.models import User


class Place(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    feedback = models.OneToOneField(Feedback, on_delete=models.CASCADE, blank=True, null=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    data = JSONField(blank=True, null=True)
    description = models.CharField(max_length=8000, blank=True, null=True)
    radius = models.FloatField(default=5.0)
    TAG_CHOICES = (
        ("hobby_related", "Hobby related"),
        ("family_related", "Family related"),
        ("education_related", "Education related"),
        ("probable_destination", "Probable destination"),
        ("checked_in", "Checked-in recently/multiply"),
        ("social_event", "Social event"),
        ("fact", "Fact"),
        ("other", "Other POI"),
    )
    tag = models.CharField(max_length=128, choices=TAG_CHOICES, default="other")
    SOURCE_CHOICES = (
        ("testimonials", "Testimonials"),
        ("facts", "Facts"),
        ("analytics", "Analytics"),
        ("social_media", "Social media"),
        ("other", "Other"),
    )
    source = models.CharField(max_length=128, choices=SOURCE_CHOICES, default="other")
    address = models.CharField(max_length=240)
    latitude = models.FloatField()
    longitude = models.FloatField()
    evaluation = models.FloatField(default=0.0)
    is_searched = models.BooleanField(default=False)
