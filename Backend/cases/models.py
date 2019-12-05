from django.db import models

from cases.utils import CaseUtils
from facilities.models import Facility
from organizations.models import Organization
from users.models import User


class Child(models.Model):

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
    PRESENCE_STATUS_CHOICES = (
        ("present", "Present"),
        ("not_present", "Not present"),
        ("transit", "Transit"),
    )
    presence_status = models.CharField(
        max_length=20, choices=PRESENCE_STATUS_CHOICES, default="present", blank=True, null=True
    )
    CASE_STATUS_CHOICES = (
        ("inactive", "Inactive"),
        ("active", "Active"),
        ("closed", "Closed"),
        ("archived", "Archived"),
    )
    status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES, default="inactive")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    description = models.CharField(max_length=5000, blank=True, null=True)
    default_message = models.CharField(max_length=5000, blank=True, null=True)
    profile_photo = models.ImageField(upload_to=CaseUtils.case_image_path, blank=True, null=True)
    has_mobile_phone = models.BooleanField(default=False)
    has_money_or_credit = models.BooleanField(default=False)
    has_area_knowledge = models.BooleanField(default=False)
    clothing_with_scent = models.BooleanField(default=False)
    rescue_teams_utilized = models.BooleanField(default=False)
    volunteers_utilized = models.BooleanField(default=False)
    organizations_cooperated = models.IntegerField(blank=True, null=True)
    transit_country = models.CharField(max_length=1000, blank=True, null=True)
    disappearance_type = models.CharField(max_length=20, blank=True, null=True)
    probable_destinations = models.CharField(max_length=5000, blank=True, null=True)
    amber_alert = models.BooleanField(default=False)

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


class FacilityReport(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    date_checked = models.DateTimeField()
    is_present = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "facility_report"


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


class DemographicData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name="demographic_data")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    home_address = models.CharField(max_length=250, blank=True, null=True)
    home_country = models.CharField(max_length=250, blank=True, null=True)
    home_postal_code = models.CharField(max_length=10, blank=True, null=True)
    home_city = models.CharField(max_length=256, blank=True, null=True)

    birth_country = models.CharField(max_length=250, blank=True, null=True)
    birth_city = models.CharField(max_length=256, blank=True, null=True)

    EDUCATION_CHOICES = (
        ("first_grade", "1st Grade"),
        ("second_grade", "2st Grade"),
        ("third_grade", "3st Grade"),
    )
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True, null=True)
    languages_spoken = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=1024, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    arrival_at_facility_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "demographic_data"
        verbose_name_plural = "demographic_data"

    def __str__(self):
        return str(self.id)


class PhysicalData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name="physical_data")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # EYE_COLOR_CHOICES = (
    #     ("blue", "Blue"),
    #     ("brown", "Brown"),
    #     ("gray", "Gray"),
    #     ("green", "Green"),
    #     ("other", "other"),
    # )
    eye_color = models.CharField(max_length=20, blank=True, null=True)
    # HAIR_COLOR_CHOICES = (
    #     ("black", "Black"),
    #     ("brown", "Brown"),
    #     ("red", "Red"),
    #     ("blond", "Blond"),
    #     ("other", "other"),
    # )
    hair_color = models.CharField(max_length=20, blank=True, null=True)
    SKIN_COLOR_CHOICES = (
        ("light_pale", "Light Pale"),
        ("pale", "Pale"),
        ("tanned", "Tanned"),
        ("brown", "Brown"),
        ("dark_brown", "Dark Brown"),
        ("black", "Black"),
        ("unknown", "Unknown"),
    )
    skin_color = models.CharField(max_length=50, choices=SKIN_COLOR_CHOICES, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    STATURE_CHOICES = (("tall", "Tall"), ("short", "Short"), ("normal", "Normal"))
    stature = models.CharField(max_length=20, choices=STATURE_CHOICES, blank=True, null=True)
    BODY_CHOICES = (("fat", "Fat"), ("slim", "Slim"), ("normal", "Normal"))
    body_type = models.CharField(max_length=20, choices=BODY_CHOICES, blank=True, null=True)
    characteristics = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        db_table = "physical_data"
        verbose_name_plural = "physical_data"

    def __str__(self):
        return str(self.id)


class PersonalData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name="personal_data")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    mother_fullname = models.CharField(max_length=50, blank=True, null=True)
    father_fullname = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = "personal_data"
        verbose_name_plural = "personal_data"

    def __str__(self):
        return str(self.id)

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class MedicalData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name="medical_data")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    HEALTH_ISSUES_CHOICES = (
        ("pathological", "Pathological"),
        ("diabetes", "Diabetes"),
        ("heart_issues", "Heart Issues"),
        ("other", "Other"),
    )
    health_issues = models.CharField(max_length=30, choices=HEALTH_ISSUES_CHOICES, blank=True, null=True)
    health_issues_description = models.CharField(max_length=5000, blank=True, null=True)
    medical_treatment_required = models.CharField(max_length=5000, blank=True, null=True)
    triggered_event = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        db_table = "medical_data"
        verbose_name_plural = "medical_data"

    def __str__(self):
        return str(self.id)


class PsychologicalData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name="psychological_data")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    concerns = models.CharField(max_length=30, blank=True, null=True)
    disappearance_reasons = models.CharField(max_length=30, blank=True, null=True)
    personality = models.CharField(max_length=30, blank=True, null=True)
    addiction = models.CharField(max_length=30, blank=True, null=True)
    family = models.CharField(max_length=30, blank=True, null=True)
    parents_profile = models.CharField(max_length=20, blank=True, null=True)
    family_members = models.IntegerField(blank=True, null=True)

    SCHOOL_GRADES_CHOICES = (
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("average", "Sufficient"),
        ("not_good", "Not good"),
        ("bad", "Bad"),
    )
    school_grades = models.CharField(max_length=50, choices=SCHOOL_GRADES_CHOICES, blank=True, null=True)

    SCHOOL_ABSENCES_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("none", "None"),
    )
    school_absences = models.CharField(max_length=50, choices=SCHOOL_ABSENCES_CHOICES, blank=True, null=True)

    hobbies = models.CharField(max_length=2048, blank=True, null=True)

    RELATIONSHIP_STATUS_CHOICES = (
        ("single", "Single"),
        ("in_relationship", "In a relationship"),
        ("complicated", "It's complicated"),
        ("broke_up", "Recently broke up"),
        ("other", "Other"),
    )
    relationship_status = models.CharField(max_length=50, choices=RELATIONSHIP_STATUS_CHOICES, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "psychological_data"
        verbose_name_plural = "psychological_data"

    def __str__(self):
        return str(self.id)


class SocialMediaData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name="social_media_data")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    has_social_profiles = models.BooleanField(default=False)
    description = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        db_table = "social_media_data"
        verbose_name_plural = "social_media_data"

    def __str__(self):
        return str(self.id)
