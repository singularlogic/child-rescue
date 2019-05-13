from rest_framework import serializers

from core.alerts.models import Alert
from core.feedbacks.models import Feedback


class AlertSerializer(serializers.ModelSerializer):

    fullname = serializers.SerializerMethodField(read_only=True)
    disappearance_date = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    eye_color = serializers.SerializerMethodField()
    hair_color = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = (
            'id', 'case', 'geolocation_point', 'latitude', 'longitude', 'address', 'radius', 'start', 'end', 'is_active', 'description', 'created_at', 'updated_at',
            'fullname', 'disappearance_date', 'date_of_birth', 'eye_color', 'hair_color', 'height', 'weight', 'image',
        )

    def get_fullname(self, alert):
        if alert.case is not None:
            return alert.case.personal_data.full_name
        else:
            return ''

    def get_disappearance_date(self, alert):
        feedbacks = Feedback.objects.filter(case=alert.case).order_by('date')
        if alert.case is not None and feedbacks is not None and len(feedbacks) > 0:
            return feedbacks[0].date
        else:
            return ''

    def get_image(self, alert):
        if alert.case is not None:
            return alert.case.profile_photo
        else:
            return ''

    def get_eye_color(self, alert):
        if alert.case is not None:
            return alert.case.physical_data.eye_color
        else:
            return ''

    def get_hair_color(self, alert):
        if alert.case is not None:
            return alert.case.physical_data.hair_color
        else:
            return ''

    def get_height(self, alert):
        if alert.case is not None:
            return alert.case.physical_data.height
        else:
            return ''

    def get_weight(self, alert):
        if alert.case is not None:
            return alert.case.physical_data.weight
        else:
            return ''

    def get_date_of_birth(self, alert):
        if alert.case is not None:
            return alert.case.demographic_data.date_of_birth
        else:
            return ''
