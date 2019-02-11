from django.db import models


class Child(models.Model):
    pass


class Case(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    area_of_disappearance = models.CharField(max_length=1024, blank=True, null=True)
    latitude_of_disappearance = models.FloatField(blank=True, null=True)
    longitude_of_disappearance = models.FloatField(blank=True, null=True)
    disappearance_date = models.DateTimeField(blank=True, null=True)
    found_date = models.DateTimeField(blank=True, null=True)
    conditions_of_disappearance = models.CharField(max_length=5000, blank=True, null=True)
    reasons_of_disappearance = models.CharField(max_length=5000, blank=True, null=True)
    CHILD_STATE_CHOICES = (
        ('abused', 'Abused'),
        ('shocked', 'Shocked'),
        ('normal', 'Normal'),
        ('dead', 'Dead'),
        ('wounded', 'Wounded'),
    )
    child_state = models.CharField(max_length=20, choices=CHILD_STATE_CHOICES, blank=True, null=True)
    has_mobile_phone = models.BooleanField(default=False)
    has_money_or_credit = models.BooleanField(default=False)
    has_area_knowledge = models.BooleanField(default=False)
    rescue_teams_utilized = models.BooleanField(default=False)
    volunteers_utilized = models.BooleanField(default=False)
    transit_country = models.CharField(max_length=1000, blank=True, null=True)
    arrival_at_facility_date = models.DateTimeField(blank=True, null=True)
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
    multi_times_case = models.IntegerField(blank=True, null=True)
    family_members = models.IntegerField(blank=True, null=True)
    probable_destinations = models.CharField(max_length=5000, blank=True, null=True)
    clothing_with_scent = models.BooleanField(default=False)


class Demographics(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, blank=True, null=True)
    home_address = models.CharField(max_length=250, blank=True, null=True)
    home_country = models.CharField(max_length=250, blank=True, null=True)
    home_postal_code = models.CharField(max_length=10, blank=True, null=True)
    home_city = models.CharField(max_length=256, blank=True, null=True)

    birth_address = models.CharField(max_length=250, blank=True, null=True)
    birth_country = models.CharField(max_length=250, blank=True, null=True)
    birth_postal_code = models.CharField(max_length=10, blank=True, null=True)
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


class Medical(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, blank=True, null=True)
    health_issues = models.CharField(max_length=2048)
    medical_treatment_required = models.BooleanField(default=False)


class Social(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, blank=True, null=True)
    social_media = models.CharField(max_length=2048, blank=True, null=True)
    CONCERN_CHOICES = (
        ('child_headed_household', 'Child headed household'),
        ('disabled', 'Disabled'),
        ('medical_case', 'Medical case'),
        ('street_child', 'Street child'),
    )
    concern = models.CharField(max_length=20, choices=CONCERN_CHOICES, blank=True, null=True)
    PSYCHOLOGY_CHOICES = (
        ('antisocial', 'Antisocial'),
        ('suicidal', 'Suicidal'),
        ('autistic', 'Autistic'),
        ('depressive', 'Depressive'),
    )
    psychology = models.CharField(max_length=20, choices=PSYCHOLOGY_CHOICES, blank=True, null=True)
    FAMILY_CHOICES = (
        ('both_parents', 'Both parents'),
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('no_parents', 'No parents'),
    )
    family = models.CharField(max_length=20, choices=FAMILY_CHOICES, blank=True, null=True)
    PARENTS_PROFILE_CHOICES = (
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('sufficient', 'Sufficient'),
        ('not_good', 'Not good'),
        ('really_bad', 'Really bad'),
    )
    parents_profile = models.CharField(max_length=20, choices=PARENTS_PROFILE_CHOICES, blank=True, null=True)
    school_grades = models.CharField(max_length=2048, blank=True, null=True)
    school_absences = models.CharField(max_length=2048, blank=True, null=True)
    hobbies = models.CharField(max_length=2048, blank=True, null=True)
    relationship_status = models.CharField(max_length=2048, blank=True, null=True)
    religion = models.CharField(max_length=2048, blank=True, null=True)


class PhysicalData(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, blank=True, null=True)
    eye_color = models.CharField(max_length=50)
    hair_color = models.CharField(max_length=50)
    skin_color = models.CharField(max_length=50)
    height = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
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
    characteristics = models.CharField(max_length=5000)


class ChildProfile(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    mobile_mother = models.CharField(max_length=15)
    mobile_father = models.CharField(max_length=15)
