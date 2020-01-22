from rest_framework import serializers

from feedbacks.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField(read_only=True)
    case = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.SerializerMethodField()
    checked_by_id = serializers.SerializerMethodField()
    checked_by_name = serializers.SerializerMethodField()
    checked_by_role = serializers.SerializerMethodField()
    alert_id = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = "__all__"

    @staticmethod
    def get_fullname(feedback):
        if feedback.case is not None:
            return feedback.case.child.full_name
        else:
            return ""

    @staticmethod
    def get_user_id(feedback):
        if feedback.user is not None:
            return feedback.user.id
        else:
            return None

    @staticmethod
    def get_checked_by_id(feedback):
        if feedback.checked_by is not None:
            return feedback.checked_by.id
        else:
            return ""

    @staticmethod
    def get_checked_by_name(feedback):
        if feedback.checked_by is not None:
            return feedback.checked_by.last_name + " " + feedback.checked_by.first_name
        else:
            return ""

    @staticmethod
    def get_checked_by_role(feedback):
        if feedback.checked_by is not None:
            return feedback.checked_by.role
        else:
            return ""

    @staticmethod
    def get_alert_id(feedback):
        if feedback.alert is not None:
            return feedback.alert.id
        else:
            return ""
