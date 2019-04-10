from django.db import models

from core.cases.utils import CaseUtils
from core.organizations.models import Organization
from core.facilities.models import Facility
from core.users.models import User


class ImageUpload(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=CaseUtils.image_upload_path, blank=True, null=True)


class Child(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'child'
        verbose_name_plural = 'children'

    def __str__(self):
        return str(self.id)


class Case(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    facility = models.ManyToManyField(Facility, through='FacilityHistory')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, blank=True, null=True)

    CASE_STATUS_CHOICES = (
        ('inactive', 'Inactive'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    )
    status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES, default='inactive')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    description = models.CharField(max_length=5000, blank=True, null=True)
    default_message = models.CharField(max_length=5000, blank=True, null=True)
    profile_photo = models.CharField(max_length=254, blank=True, null=True)
    has_mobile_phone = models.BooleanField(default=False)
    has_money_or_credit = models.BooleanField(default=False)
    has_area_knowledge = models.BooleanField(default=False)
    rescue_teams_utilized = models.BooleanField(default=False)
    volunteers_utilized = models.BooleanField(default=False)
    organizations_cooperated = models.IntegerField(blank=True, null=True)
    transit_country = models.CharField(max_length=1000, blank=True, null=True)
    DISAPPEARANCE_TYPE_CHOICES = (
        ('runaway', 'Runaway'),
        ('parental', 'Parental'),
        ('abduction', 'Abduction'),
        ('criminal', 'Criminal'),
        ('missing', 'Missing'),
        ('minor', 'Minor'),
        ('tracing', 'Tracing'),
        ('request', 'Request'),
        ('unclear', 'Unclear'),
    )
    disappearance_type = models.CharField(max_length=20, choices=DISAPPEARANCE_TYPE_CHOICES, blank=True, null=True)
    probable_destinations = models.CharField(max_length=5000, blank=True, null=True)
    clothing_with_scent = models.BooleanField(default=False)
    amber_alert = models.BooleanField(default=False)

    class Meta:
        db_table = 'case'
        verbose_name_plural = 'cases'

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


class FacilityHistory(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    date_entered = models.DateTimeField()
    date_left = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'facility_history'


class FacilityReport(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    date_checked = models.DateTimeField()
    is_present = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'facility_report'


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'case_follower'


class DemographicData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name='demographic_data')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    home_address = models.CharField(max_length=250, blank=True, null=True)
    home_country = models.CharField(max_length=250,  blank=True, null=True)
    home_postal_code = models.CharField(max_length=10, blank=True, null=True)
    home_city = models.CharField(max_length=256, blank=True, null=True)

    birth_country = models.CharField(max_length=250, blank=True, null=True)
    birth_city = models.CharField(max_length=256, blank=True, null=True)

    EDUCATION_CHOICES = (
        ('first_grade', '1st Grade'),
        ('second_grade', '2st Grade'),
        ('third_grade', '3st Grade'),
        ('unknown', 'Unknown'),
    )
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True, null=True)
    languages_spoken = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=1024, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    arrival_at_facility_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'demographic_data'
        verbose_name_plural = 'demographic_data'

    def __str__(self):
        return str(self.id)


class PhysicalData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name='physical_data')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    EYE_COLOR_CHOICES = (
        ('blue', 'Blue'),
        ('brown', 'Brown'),
        ('gray', 'Gray'),
        ('green', 'Green'),
        ('other', 'other'),
    )
    eye_color = models.CharField(max_length=20, choices=EYE_COLOR_CHOICES, blank=True, null=True)
    HAIR_COLOR_CHOICES = (
        ('black', 'Black'),
        ('brown', 'Brown'),
        ('red', 'Red'),
        ('blond', 'Blond'),
        ('other', 'other'),
    )
    hair_color = models.CharField(max_length=20, choices=HAIR_COLOR_CHOICES, blank=True, null=True)
    SKIN_COLOR_CHOICES = (
        ('white', 'White'),
        ('brown', 'Brown'),
        ('dark', 'Dark'),
        ('other', 'other'),
    )
    skin_color = models.CharField(max_length=50, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    STATURE_CHOICES = (
        ('tall', 'Tall'),
        ('short', 'Short'),
        ('normal', 'Normal'),
    )
    stature = models.CharField(max_length=20, choices=STATURE_CHOICES, blank=True, null=True)
    BODY_CHOICES = (
        ('fat', 'Fat'),
        ('slim', 'Slim'),
        ('normal', 'Normal'),
    )
    body_type = models.CharField(max_length=20, choices=BODY_CHOICES, blank=True, null=True)
    characteristics = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        db_table = 'physical_data'
        verbose_name_plural = 'physical_data'

    def __str__(self):
        return str(self.id)


class PersonalData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name='personal_data')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    mother_fullname = models.CharField(max_length=50, blank=True, null=True)
    father_fullname = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    mobile_mother = models.CharField(max_length=15, blank=True, null=True)
    mobile_father = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'personal_data'
        verbose_name_plural = 'personal_data'

    def __str__(self):
        return str(self.id)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


class MedicalData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name='medical_data')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    HEALTH_ISSUES_CHOICES = (
        ('pathological', 'Pathological'),
        ('diabetes', 'Diabetes'),
        ('heart_issues', 'Heart Issues'),
        ('other', 'Other'),
    )
    health_issues = models.CharField(max_length=30, choices=HEALTH_ISSUES_CHOICES, blank=True, null=True)
    health_issues_description = models.CharField(max_length=5000, blank=True, null=True)
    medical_treatment_required = models.BooleanField(default=False)

    class Meta:
        db_table = 'medical_data'
        verbose_name_plural = 'medical_data'

    def __str__(self):
        return str(self.id)


class PsychologicalData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name='psychological_data')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    CONCERN_CHOICES = (
        ('child_headed_household', 'Child headed household'),
        ('disabled', 'Disabled'),
        ('medical_case', 'Medical case'),
        ('street_child', 'Street child'),
    )
    concerns = models.CharField(max_length=30, choices=CONCERN_CHOICES, blank=True, null=True)

    PERSONALITY_CHOICES = (
        ('antisocial', 'Antisocial'),
        ('suicidal', 'Suicidal'),
        ('autistic', 'Autistic'),
        ('depressive', 'Depressive'),
    )
    personality = models.CharField(max_length=30, choices=PERSONALITY_CHOICES, blank=True, null=True)

    FAMILY_CHOICES = (
        ('both_parents', 'Both parents'),
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('no_parents', 'No parents'),
    )
    family = models.CharField(max_length=30, choices=FAMILY_CHOICES, blank=True, null=True)

    PARENTS_PROFILE_CHOICES = (
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('sufficient', 'Sufficient'),
        ('not_good', 'Not good'),
        ('really_bad', 'Really bad'),
        ('unknown', 'Unknown'),
    )
    mothers_profile = models.CharField(max_length=20, choices=PARENTS_PROFILE_CHOICES, blank=True, null=True)
    fathers_profile = models.CharField(max_length=20, choices=PARENTS_PROFILE_CHOICES, blank=True, null=True)

    family_members = models.IntegerField(blank=True, null=True)

    SCHOOL_GRADES_CHOICES = (
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Sufficient'),
        ('not_good', 'Not good'),
        ('bad', 'Bad'),
    )
    school_grades = models.CharField(max_length=50, choices=SCHOOL_GRADES_CHOICES, blank=True, null=True)

    SCHOOL_ABSENCES_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('none', 'None'),
        ('unknown', 'Unknown'),
    )
    school_absences = models.CharField(max_length=50, choices=SCHOOL_ABSENCES_CHOICES, blank=True, null=True)

    hobbies = models.CharField(max_length=2048, blank=True, null=True)

    RELATIONSHIP_STATUS_CHOICES = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('other', 'Other'),
    )
    relationship_status = models.CharField(max_length=50, choices=RELATIONSHIP_STATUS_CHOICES, blank=True, null=True)

    RELIGION_CHOICES = (
        ('christian', 'Christian'),
        ('muslim', 'Muslim'),
        ('atheist', 'Atheist'),
        ('other', 'Other'),
    )
    religion = models.CharField(max_length=50, choices=RELIGION_CHOICES, blank=True, null=True)

    class Meta:
        db_table = 'psychological_data'
        verbose_name_plural = 'psychological_data'

    def __str__(self):
        return str(self.id)


class SocialMediaData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name='social_media_data')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    has_social_profiles = models.BooleanField(default=False)
    description = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        db_table = 'social_media_data'
        verbose_name_plural = 'social_media_data'

    def __str__(self):
        return str(self.id)


