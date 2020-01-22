import os
from django.conf import settings
from rest_framework import serializers

from cases.models import Case, SocialMedia, Follower, CaseVolunteer, CaseVolunteerLocation, Feed, FacilityHistory
from facilities.models import Facility
from feedbacks.models import Feedback


class SocialMediaSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SocialMedia
        fields = "__all__"

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child


# class CaseSerializer(serializers.ModelSerializer):
#     social_media_data = SocialMediaDataSerializer()
#
#     class Meta:
#         model = Case
#         fields = "__all__"


class CaseSerializer(serializers.ModelSerializer):

    social_media = SocialMediaSerializer(write_only=True)
    disappearance_date = serializers.SerializerMethodField(read_only=True)
    disappearance_location = serializers.SerializerMethodField(read_only=True)
    arrival_date = serializers.SerializerMethodField()

    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    father_fullname = serializers.SerializerMethodField()
    mother_fullname = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()

    current_facility_id = serializers.SerializerMethodField(read_only=True)
    current_facility = serializers.SerializerMethodField(read_only=True)
    current_facility_id_ref = None

    class Meta:
        model = Case
        fields = "__all__"

    def get_current_facility_id(self, case):
        try:
            current_facility = FacilityHistory.objects.get(case=case, is_active=True)
            self.current_facility_id_ref = current_facility.facility.id
            return current_facility.facility.id
        except FacilityHistory.DoesNotExist:
            return None

    def get_current_facility(self, case):
        try:
            current_facility = Facility.objects.get(id=self.current_facility_id_ref)
            self.current_facility_id_ref = None
            return current_facility.name
        except Facility.DoesNotExist:
            return None

    @staticmethod
    def get_gender(case):
        return case.child.gender

    @staticmethod
    def get_arrival_date(case):
        return case.arrival_at_facility_date

    @staticmethod
    def get_first_name(case):
        return case.child.first_name

    @staticmethod
    def get_father_fullname(case):
        return case.child.father_fullname

    @staticmethod
    def get_mother_fullname(case):
        return case.child.mother_fullname

    @staticmethod
    def get_last_name(case):
        return case.child.last_name

    @staticmethod
    def get_phone(case):
        return case.child.phone

    @staticmethod
    def get_date_of_birth(case):
        return case.child.date_of_birth

    @staticmethod
    def get_disappearance_date(case):
        feedbacks = Feedback.objects.filter(case=case).order_by("id")
        if case is not None and feedbacks is not None and len(feedbacks) > 0:
            return feedbacks[0].date
        else:
            return ""

    @staticmethod
    def get_disappearance_location(case):
        feedbacks = Feedback.objects.filter(case=case).order_by("date")
        if case is not None and feedbacks is not None and len(feedbacks) > 0:
            return feedbacks[0].address
        else:
            return ""


class FeedSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = "__all__"

    @staticmethod
    def get_name(feed):
        return feed.user.first_name + " " + feed.user.last_name


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"


class CaseVolunteerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    child_name = serializers.SerializerMethodField()
    is_amber_alert = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = CaseVolunteer
        fields = "__all__"

    @staticmethod
    def get_image(case_volunteer):
        return (
            os.path.join(settings.BASE_URL + "media/", str(case_volunteer.case.profile_photo))
            if case_volunteer.case.profile_photo
            else None
        )

    @staticmethod
    def get_child_name(case_volunteer):
        return case_volunteer.case.child.full_name

    @staticmethod
    def get_is_amber_alert(case_volunteer):
        return case_volunteer.case.amber_alert

    @staticmethod
    def get_first_name(case_volunteer):
        return case_volunteer.user.first_name

    @staticmethod
    def get_last_name(case_volunteer):
        return case_volunteer.user.last_name

    @staticmethod
    def get_email(case_volunteer):
        return case_volunteer.user.email


class CaseVolunteerLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseVolunteerLocation
        fields = "__all__"
