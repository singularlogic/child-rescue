from rest_framework import serializers
import os

from alerts.models import Alert
from feedbacks.models import Feedback


class AlertSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField(read_only=True)
    disappearance_date = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    eye_color = serializers.SerializerMethodField()
    hair_color = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    stature = serializers.SerializerMethodField()
    body_type = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()
    haircut = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = (
            "id",
            "case",
            "geolocation_point",
            "latitude",
            "longitude",
            "address",
            "radius",
            "start",
            "end",
            "is_active",
            "description",
            "created_at",
            "updated_at",
            "fullname",
            "disappearance_date",
            "date_of_birth",
            "eye_color",
            "hair_color",
            "height",
            "weight",
            "image",
            "stature",
            "body_type",
            "haircut",
        )

    @staticmethod
    def get_fullname(alert):
        # Careful here it is custom_name instead fullname
        if alert.case is not None:
            return alert.case.custom_name
        else:
            return ""

    @staticmethod
    def get_haircut(alert):
        # Careful here it is custom_name instead fullname
        if alert.case is not None:
            return alert.case.haircut
        else:
            return ""

    @staticmethod
    def get_disappearance_date(alert):
        feedbacks = Feedback.objects.filter(case=alert.case).order_by("date")
        if alert.case is not None and feedbacks is not None and len(feedbacks) > 0:
            return feedbacks[0].date
        else:
            return ""

    # @staticmethod
    # def get_image(alert):
    #     if alert.case is not None:
    #         return os.getenv("BASE_URL") + "media/" + str(alert.case.profile_photo)
    #     else:
    #         return ""

    def get_image(self, alert):
        request = self.context.get("request")
        photo = alert.case.profile_photo
        if photo and photo is not None:
            return request.build_absolute_uri(photo.url)
        return None

    @staticmethod
    def get_eye_color(alert):
        if alert.case is not None:
            return alert.case.eye_color
        else:
            return ""

    @staticmethod
    def get_stature(alert):
        if alert.case is not None:
            return alert.case.stature
        else:
            return ""

    @staticmethod
    def get_body_type(alert):
        if alert.case is not None:
            return alert.case.body_type
        else:
            return ""

    @staticmethod
    def get_hair_color(alert):
        if alert.case is not None:
            return alert.case.hair_color
        else:
            return ""

    @staticmethod
    def get_height(alert):
        if alert.case is not None:
            return alert.case.height
        else:
            return ""

    @staticmethod
    def get_weight(alert):
        if alert.case is not None:
            return alert.case.weight
        else:
            return ""

    @staticmethod
    def get_date_of_birth(alert):
        if alert.case is not None:
            return alert.case.child.date_of_birth
        else:
            return ""
