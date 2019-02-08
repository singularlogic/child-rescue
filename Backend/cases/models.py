from django.db import models


class Case(models.Model):
    latitude_of_disappearance = models.FloatField()
    longitude_of_disappearance = models.FloatField()
    disappearance_date = models.DateTimeField(blank=True, null=True)
    found_date = models.DateTimeField(blank=True, null=True)
    conditions_of_disappearance = models.CharField(max_length=5000)
    reasons_of_disappearance = models.CharField(max_length=5000)
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
    transit_country = models.CharField(max_length=1000)
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
    multi_times_case = models.IntegerField()
    family_members = models.IntegerField()
    probable_destinations = models.CharField(max_length=5000)
    clothing_with_scent = models.BooleanField(default=False)


class Child(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    mobile_mother = models.CharField(max_length=15)
    mobile_father = models.CharField(max_length=15)
    eye_color = models.CharField(max_length=50)
    hair_color = models.CharField(max_length=50)
    skin_color = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    height = models.CharField(max_length=50)
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
    facebook = models.CharField(max_length=256)
    # STATURE_CHOICES = (
    #     ('tall', 'Tall'),
    #     ('short', 'Short'),
    #     ('normal', 'Normal'),
    # )
    # stature = models.CharField(max_length=20, choices=STATURE_CHOICES, blank=True, null=True)
