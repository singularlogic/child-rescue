from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.gis.db import models as geo_models
from django.db.models.signals import post_save
from django.dispatch import receiver

from blockchain.blockchain import createCase
from cases.utils import CaseUtils
from facilities.models import Facility
from organizations.models import Organization
from users.models import User


class Child(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    mother_fullname = models.CharField(max_length=50, blank=True, null=True)
    father_fullname = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, choices=CaseUtils.GENDER_CHOICES, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "child"
        verbose_name_plural = "children"

    def __str__(self):
        return str(self.id)


class Case(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    facility = models.ManyToManyField(Facility, through="FacilityHistory")
    child = models.ForeignKey(Child, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")
    user = models.ManyToManyField(User, through="CaseVolunteer")
    data = JSONField(blank=True, null=True)
    custom_name = models.CharField(max_length=100, blank=True, null=True)
    blockchain_address = models.CharField(max_length=256, blank=True, null=True)
    presence_status = models.CharField(
        max_length=20, choices=CaseUtils.PRESENCE_STATUS_CHOICES, default="present", blank=True, null=True
    )
    status = models.CharField(max_length=20, choices=CaseUtils.CASE_STATUS_CHOICES, default="active")
    arrival_at_facility_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    default_message = models.CharField(max_length=5000, blank=True, null=True)
    profile_photo = models.ImageField(upload_to=CaseUtils.case_image_path, blank=True, null=True)

    has_mobile_phone = models.CharField(max_length=20, choices=CaseUtils.MOBILE_CHOICES, blank=True, null=True)
    has_money_or_credit = models.CharField(
        max_length=20, choices=CaseUtils.BOOLEAN_POSSIBLE_2_DATA_CHOICES, blank=True, null=True
    )
    has_area_knowledge = models.CharField(max_length=20, choices=CaseUtils.BOOLEAN_DATA_CHOICES, blank=True, null=True)
    clothing_with_scent = models.CharField(max_length=20, choices=CaseUtils.BOOLEAN_DATA_CHOICES, blank=True, null=True)

    rescue_teams_utilized = models.BooleanField(default=False)
    volunteers_utilized = models.BooleanField(default=False)
    transit_country = models.CharField(max_length=1000, blank=True, null=True)
    disappearance_type = models.CharField(
        max_length=20, choices=CaseUtils.DISAPPEARANCE_TYPE_CHOICES, blank=True, null=True
    )
    amber_alert = models.BooleanField(default=False)
    eye_color = models.CharField(max_length=20, blank=True, null=True)
    hair_color = models.CharField(max_length=20, blank=True, null=True)
    skin_color = models.CharField(max_length=50, choices=CaseUtils.SKIN_COLOR_CHOICES, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    stature = models.CharField(max_length=20, choices=CaseUtils.STATURE_CHOICES, blank=True, null=True)
    body_type = models.CharField(max_length=20, choices=CaseUtils.BODY_CHOICES, blank=True, null=True)
    haircut = models.CharField(max_length=20, blank=True, null=True)
    characteristics = models.CharField(max_length=5000, blank=True, null=True)
    home_address = models.CharField(max_length=250, blank=True, null=True)
    home_country = models.CharField(max_length=250, blank=True, null=True)
    home_postal_code = models.CharField(max_length=10, blank=True, null=True)
    birth_country = models.CharField(max_length=250, blank=True, null=True)
    education_level = models.CharField(max_length=20, choices=CaseUtils.EDUCATION_CHOICES, blank=True, null=True)
    languages_spoken = models.CharField(max_length=250, blank=True, null=True)
    nationality = models.CharField(max_length=1024, blank=True, null=True)
    addiction = models.CharField(max_length=30, choices=CaseUtils.BOOLEAN_DATA_CHOICES, blank=True, null=True)
    health_issues = models.CharField(max_length=30, choices=CaseUtils.BOOLEAN_DATA_CHOICES, blank=True, null=True)
    medical_treatment_required = models.CharField(
        max_length=30, choices=CaseUtils.BOOLEAN_DATA_CHOICES, blank=True, null=True
    )
    health_issues_description = models.CharField(max_length=5000, blank=True, null=True)
    triggered_event = models.CharField(max_length=30, choices=CaseUtils.BOOLEAN_DATA_CHOICES, blank=True, null=True)
    concerns = models.CharField(max_length=30, choices=CaseUtils.CONCERN_CHOICES, blank=True, null=True)
    mental_disorders = models.CharField(max_length=30, choices=CaseUtils.DISORDERS_CHOICES, blank=True, null=True)
    psychological_disorders = models.CharField(
        max_length=30, choices=CaseUtils.DISORDERS_CHOICES, blank=True, null=True
    )
    physical_disabilities = models.CharField(
        max_length=30, choices=CaseUtils.BOOLEAN_DATA_CHOICES, blank=True, null=True
    )
    living_environment = models.CharField(
        max_length=30, choices=CaseUtils.LIVING_ENVIRONMENT_CHOICES, blank=True, null=True
    )
    family_members = models.IntegerField(blank=True, null=True)
    school_grades = models.CharField(max_length=50, choices=CaseUtils.SCHOOL_GRADES_CHOICES, blank=True, null=True)
    hobbies = models.CharField(max_length=2048, blank=True, null=True)
    relationship_status = models.CharField(
        max_length=50, choices=CaseUtils.RELATIONSHIP_STATUS_CHOICES, blank=True, null=True
    )
    religion = models.CharField(max_length=50, blank=True, null=True)
    disappearance_reasons = models.CharField(
        max_length=30, choices=CaseUtils.DISAPPEARANCE_REASON_CHOICES, blank=True, null=True
    )
    parents_profile = models.CharField(max_length=20, choices=CaseUtils.PARENTS_PROFILE_CHOICES, blank=True, null=True)
    is_high_risk = models.CharField(
        max_length=20, choices=CaseUtils.BOOLEAN_POSSIBLE_DATA_CHOICES, blank=True, null=True
    )
    is_first_time_missing = models.CharField(
        max_length=20, choices=CaseUtils.BOOLEAN_DATA_CHOICES, blank=True, null=True
    )
    has_trafficking_history = models.CharField(
        max_length=20, choices=CaseUtils.BOOLEAN_POSSIBLE_DATA_CHOICES, blank=True, null=True
    )
    is_refugee = models.CharField(max_length=20, choices=CaseUtils.BOOLEAN_DATA_CHOICES, blank=True, null=True)
    legal_status = models.CharField(max_length=20, choices=CaseUtils.LEGAL_STATUS_CHOICES, blank=True, null=True)
    contacted_date = models.DateField(blank=True, null=True)
    risk_indicator = models.FloatField(default=0.0)
    days_diff = models.FloatField(default=0.0)
    go_missing_possibility = models.FloatField(default=0.0)
    current_mindset = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = "case"
        verbose_name_plural = "cases"

    def __str__(self):
        return str(self.id)

    @staticmethod
    def get_web_queryset(child_id=None, organization_id=None):
        if child_id:
            if organization_id is not None:
                return Case.objects.filter(child_id=child_id, organization_id=organization_id)
            else:
                return Case.objects.filter(child_id=child_id)
        else:
            if organization_id is not None:
                return Case.objects.filter(organization_id=organization_id)
            else:
                return Case.objects.all()


@receiver(post_save, sender=Case, dispatch_uid="update_case_blockchain")
def update_case_blockchain(sender, instance, **kwargs):
    if instance.blockchain_address is None:
        blockchain_address = createCase(instance.status)
        instance.blockchain_address = blockchain_address
        instance.save()


class SocialMedia(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="social_media")
    medium = models.CharField(max_length=120, blank=True, null=True)
    published_photos = models.CharField(
        max_length=20, choices=CaseUtils.BOOLEAN_DATA_CHOICES, blank=True, null=True, default=None
    )
    followers = models.CharField(
        max_length=20, choices=CaseUtils.FOLLOWERS_CHOICES, blank=True, null=True, default=None
    )
    recent_activity = models.CharField(
        max_length=20, choices=CaseUtils.RECENT_ACTIVITY_CHOICES, blank=True, null=True, default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "social_media"
        verbose_name_plural = "social_media"

    def __str__(self):
        return "Case: {} - Medium: {}".format(self.case, self.medium)


class SocialNetworksData(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=500, blank=True, null=True)
    SOURCE_CHOICES = (
        ("eventful", "Eventful"),
        ("foursquare", "Foursquare"),
        ("twitter", "Twitter"),
        ("google", "Google"),
        ("other", "Other"),
    )
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="eventful")
    geolocation_point = geo_models.PointField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=500, blank=True, null=True)
    venue = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    start = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    description = models.CharField(max_length=4096, blank=True, null=True)
    TAG_CHOICES = (
        ("announcement", "Announcement"),
        ("task", "Task"),
        ("fact", "Fact"),
        ("general", "General"),
    )
    tag = models.CharField(max_length=128, choices=TAG_CHOICES, default="general")
    is_visible_to_volunteers = models.BooleanField(default=False)
    image = models.ImageField(upload_to=CaseUtils.feed_image_path, blank=True, null=True)
    address = models.CharField(max_length=240, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    radius = models.FloatField(default=5.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "feed"
        verbose_name_plural = "feed"


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    title = models.CharField(max_length=240)
    image = models.ImageField(upload_to=CaseUtils.file_image_path, blank=True, null=True)
    file = models.FileField(upload_to=CaseUtils.file_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "file"
        verbose_name_plural = "file"


class FacilityHistory(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    date_entered = models.DateTimeField()
    date_left = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "facility_history"
        verbose_name_plural = "facility_history"


class FacilityReport(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    date_checked = models.DateTimeField()
    is_present = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "facility_report"
        verbose_name_plural = "facility_reports"


class CaseVolunteer(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    has_accept_invitation = models.NullBooleanField(default=None)
    is_team_leader = models.NullBooleanField(default=False)
    team_name = models.CharField(max_length=256, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "case_volunteer"
        verbose_name_plural = "case_volunteers"
        unique_together = (
            "case",
            "user",
        )


class CaseVolunteerLocation(models.Model):
    case_volunteer = models.ForeignKey(CaseVolunteer, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "case_volunteer_location"
        verbose_name_plural = "case_volunteer_locations"


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "case_follower"
        verbose_name_plural = "case_followers"
        unique_together = ("user", "case")
