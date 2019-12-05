import os
from django.conf import settings
from rest_framework import serializers

from cases.models import (
    DemographicData,
    MedicalData,
    PsychologicalData,
    PhysicalData,
    PersonalData,
    Case,
    SocialMediaData,
    Follower,
    CaseVolunteer, CaseVolunteerLocation, Feed)


class DemographicDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child

    class Meta:
        model = DemographicData
        fields = "__all__"


class MedicalDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MedicalData
        fields = "__all__"

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child


class PsychologicalDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PsychologicalData
        fields = "__all__"

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child


class PhysicalDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PhysicalData
        fields = "__all__"

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child


class PersonalDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PersonalData
        fields = "__all__"

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child


class SocialMediaDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SocialMediaData
        fields = "__all__"

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child


class CaseSerializer(serializers.ModelSerializer):

    demographic_data = DemographicDataSerializer()
    medical_data = MedicalDataSerializer()
    psychological_data = PsychologicalDataSerializer()
    physical_data = PhysicalDataSerializer()
    personal_data = PersonalDataSerializer()
    social_media_data = SocialMediaDataSerializer()

    class Meta:
        model = Case
        fields = "__all__"


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

    class Meta:
        model = CaseVolunteer
        fields = "__all__"

    @staticmethod
    def get_image(case_volunteer):
        return os.path.join(settings.BASE_URL+'media/', str(case_volunteer.case.profile_photo)) if case_volunteer.case.profile_photo else None

    @staticmethod
    def get_child_name(case_volunteer):
        return case_volunteer.case.personal_data.full_name

    @staticmethod
    def get_is_amber_alert(case_volunteer):
        return case_volunteer.case.amber_alert


class CaseVolunteerLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseVolunteerLocation
        fields = "__all__"
