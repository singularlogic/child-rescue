from rest_framework import serializers

from alerts.models import Alert
from feedbacks.models import Feedback


class AlertSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField(read_only=True)
    custom_name = serializers.SerializerMethodField(read_only=True)
    disappearance_date = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    eye_color = serializers.SerializerMethodField()
    hair_color = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    haircut = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = "__all__"

    @staticmethod
    def get_fullname(alert):
        if alert.case is not None:
            return alert.case.child.full_name
        else:
            return ""

    @staticmethod
    def get_organization_name(alert):
        return alert.organization.name

    @staticmethod
    def get_haircut(alert):
        # Careful here it is custom_name instead fullname
        if alert.case is not None:
            return alert.case.haircut
        else:
            return ""

    @staticmethod
    def get_custom_name(alert):
        if alert.case is not None:
            return alert.case.custom_name
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
    #         import os

    #         return os.getenv("BASE_URL") + "media/" + str(alert.case.profile_photo)
    #         # return "http://localhost:8000/media/" + str(alert.case.profile_photo)
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
