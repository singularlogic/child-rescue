from django.db import models

from core.users.models import User


class FCMDevice(models.Model):
    DEVICE_TYPES = (
        (u'ios', u'ios'),
        (u'android', u'android'),
        (u'web', u'web')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='device', blank=True, null=True)
    registration_id = models.TextField()
    type = models.CharField(choices=DEVICE_TYPES, max_length=10)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'FCM device'

    def __str__(self):
        return 'uuid: {} - registration_id: {}'.format(self.uuid.id, self.registration_id)
