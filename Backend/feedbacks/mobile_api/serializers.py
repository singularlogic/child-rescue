from rest_framework import serializers

from feedbacks.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    checked_by_id = serializers.SerializerMethodField()
    checked_by_name = serializers.SerializerMethodField()
    alert_id = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = (
            "id",
            "user",
            "source",
            "latitude",
            "longitude",
            "date",
            "current_latitude",
            "current_longitude",
            "comment",
            "feedback_image",
            "address",
            "created_at",
            "updated_at",
            "checked_by_id",
            "checked_by_name",
            "checked_on",
            "feedback_status",
            "is_valid",
            "location_selected_reasons",
            "child_status",
            "transportation",
            "case",
            "alert_id",
        )

    def get_checked_by_id(self, feedback):
        if feedback.checked_by is not None:
            return feedback.checked_by.id
        else:
            return ""

    def get_checked_by_name(self, feedback):
        if feedback.checked_by is not None:
            return feedback.checked_by.last_name + " " + feedback.checked_by.first_name
        else:
            return ""

    def get_alert_id(self, feedback):
        if feedback.alert is not None:
            return feedback.alert.id
        else:
            return ""


# class ImageUploadSerializer(serializers.Serializer):
#     class Meta:
#         model = ImageUpload
#         fields = '__all__'
