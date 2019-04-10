from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from core.organizations.models import Organization
from core.facilities.models import Facility
from .utils import profile_image_path
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT, blank=True, null=True)
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('owner', 'Owner'),
        ('coordinator', 'Coordinator'),
        ('case_manager', 'Case Manager'),
        ('network_manager', 'Network Manager'),
        ('facility_manager', 'Facility Manager'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    is_private_account = models.BooleanField(default=False)
    is_geolocation_shared = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to=profile_image_path, blank=True, null=True)

    def profile_image_element(self):
        return mark_safe('<img src="http://localhost:8000/media/%s" width="16" height="16" />' % self.profile_image)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into the admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_end_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.email


class Uuid(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    value = models.CharField(max_length=500)

    class Meta:
        db_table = 'uuid'

    def __str__(self):
        return '{} - {}'.format(self.id, self.value)


class UuidActivity(models.Model):
    uuid = models.ForeignKey(Uuid, on_delete=models.CASCADE)

    action = models.CharField(max_length=30)
    params = models.CharField(max_length=1000, blank=True, null=True)
    device = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'uuid_activity'

    def __str__(self):
        return '{}'.format(self.id)
