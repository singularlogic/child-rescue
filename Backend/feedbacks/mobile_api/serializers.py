from rest_framework import serializers

from feedbacks.models import Feedback


class CreateFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField()
    alert_id = serializers.SerializerMethodField()
    child_id = serializers.SerializerMethodField()
    child_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = (
            "id",
            "alert_id",
            "feedback_image",
            "address",
            "child_id",
            "child_full_name",
            "profile_photo",
            "comment",
            "created_at",
        )

    @staticmethod
    def get_child_id(feedback):
        return feedback.case.child.id

    @staticmethod
    def get_child_full_name(feedback):
        return feedback.case.child.full_name

    # @staticmethod
    # def get_profile_photo(feedback):
    #     return feedback.case.profile_photo.url

    def get_profile_photo(self, instance):
        if not instance.case.profile_photo:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(instance.case.profile_photo.url)

    @staticmethod
    def get_alert_id(feedback):
        if feedback.alert is not None:
            return feedback.alert.id
        else:
            return ""

    # def get_image(self, alert):
    #     request = self.context.get("request")
    #     photo = alert.case.profile_photo
    # if photo is not None:
    #     return request.build_absolute_uri(photo.url)
    # return None
