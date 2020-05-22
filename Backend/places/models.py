from django.contrib.postgres.fields import JSONField
from django.db import models

from cases.models import Case
from feedbacks.models import Feedback
from users.models import User


class Place(models.Model):
    is_event = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    feedback = models.OneToOneField(Feedback, on_delete=models.CASCADE, blank=True, null=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    data = JSONField(blank=True, null=True)
    description = models.CharField(max_length=8000, blank=True, null=True)
    radius = models.FloatField(default=0.1)
    TAG_CHOICES = (
        ("asylum_related", "Hosting Facility/Asylum related"),
        ("romance_related", "Romance related"),
        ("health_related", "Hospital/Health related"),
        ("transport_related", "Public Transport related"),
        ("isolation_related", "Rural/Forest/Isolated Area"),
        ("streets_related", "On The Streets"),
        ("social_related", "Social Event/Amusement Place"),
        ("family_related", "Family/Relatives/Friend property"),
        ("education_related", "Education/Sports related"),
        ("other", "Other/Unknown"),
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
