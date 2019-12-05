from django.conf.locale import id
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from cases.models import (
    DemographicData,
    MedicalData,
    PsychologicalData,
    PhysicalData,
    PersonalData,
    Case,
    SocialMediaData,
    Child,
    FacilityHistory,
    CaseVolunteer,
    File,
    Feed,
    CaseVolunteerLocation,
)
from facilities.models import Facility
from feedbacks.models import Feedback


class FeedSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = "__all__"

    @staticmethod
    def get_name(feed):
        return feed.user.first_name + " " + feed.user.last_name

    @staticmethod
    def get_role(feed):
        return feed.user.role


class FileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = "__all__"

    @staticmethod
    def get_tag(file):
        return file.user.role if file.user else ""

    @staticmethod
    def get_first_name(file):
        return file.user.first_name if file.user else ""

    @staticmethod
    def get_last_name(file):
        return file.user.last_name if file.user else ""


class CaseVolunteerSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = CaseVolunteer
        fields = "__all__"

    @staticmethod
    def get_email(case_volunteer):
        return case_volunteer.user.email

    @staticmethod
    def get_first_name(case_volunteer):
        return case_volunteer.user.first_name

    @staticmethod
    def get_last_name(case_volunteer):
        return case_volunteer.user.last_name

    @staticmethod
    def get_city(case_volunteer):
        return case_volunteer.user.city

    @staticmethod
    def get_latitude(case_volunteer):
        last_locations = CaseVolunteerLocation.objects.filter(case_volunteer=case_volunteer.id)
        return last_locations.last().latitude if len(last_locations) > 0 else None

    @staticmethod
    def get_longitude(case_volunteer):
        last_locations = CaseVolunteerLocation.objects.filter(case_volunteer=case_volunteer.id)
        return last_locations.last().longitude if len(last_locations) > 0 else None


class DemographicDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DemographicData
        fields = (
            "id",
            "case",
            "home_address",
            "home_country",
            "home_city",
            "birth_country",
            "birth_city",
            "education_level",
            "languages_spoken",
            "nationality",
            "date_of_birth",
            "gender",
            "arrival_at_facility_date",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def get_case(instance):
        return instance.case

    @staticmethod
    def get_child(instance):
        return instance.case.child


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
    # school_grades = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PsychologicalData
        fields = "__all__"


class PhysicalDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PhysicalData
        fields = (
            "id",
            "case",
            "eye_color",
            "hair_color",
            "skin_color",
            "height",
            "weight",
            "stature",
            "body_type",
            "characteristics",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def get_case(instance):
        return instance.case

    @staticmethod
    def get_child(instance):
        return instance.case.child


class PersonalDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PersonalData
        fields = (
            "id",
            "case",
            "first_name",
            "last_name",
            "full_name",
            "mother_fullname",
            "father_fullname",
            "phone",
        )

    @staticmethod
    def get_case(instance):
        return instance.case

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


class CasesSerializer(serializers.ModelSerializer):

    demographic_data = DemographicDataSerializer(write_only=True)
    medical_data = MedicalDataSerializer(write_only=True)
    psychological_data = PsychologicalDataSerializer(write_only=True)
    physical_data = PhysicalDataSerializer(write_only=True)
    personal_data = PersonalDataSerializer(write_only=True)
    social_media_data = SocialMediaDataSerializer(write_only=True)
    disappearance_date = serializers.SerializerMethodField(read_only=True)
    disappearance_location = serializers.SerializerMethodField(read_only=True)
    arrival_date = serializers.SerializerMethodField()

    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    nationality = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    medical_treatment_required = serializers.SerializerMethodField()

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

    def get_nationality(self, case):
        return case.demographic_data.nationality

    def get_medical_treatment_required(self, case):
        return case.medical_data.medical_treatment_required

    def get_gender(self, case):
        return case.demographic_data.gender

    def get_arrival_date(self, case):
        return case.demographic_data.arrival_at_facility_date

    def get_first_name(self, case):
        return case.personal_data.first_name

    def get_last_name(self, case):
        return case.personal_data.last_name

    def get_disappearance_date(self, case):
        feedbacks = Feedback.objects.filter(case=case).order_by("id")
        if case is not None and feedbacks is not None and len(feedbacks) > 0:
            return feedbacks[0].date
        else:
            return ""

    def get_disappearance_location(self, case):
        feedbacks = Feedback.objects.filter(case=case).order_by("date")
        if case is not None and feedbacks is not None and len(feedbacks) > 0:
            return feedbacks[0].address
        else:
            return ""

    def create(self, validated_data):

        demographic_data = validated_data.pop("demographic_data")
        medical_data = validated_data.pop("medical_data")
        psychological_data = validated_data.pop("psychological_data")

        physical_data = validated_data.pop("physical_data")
        personal_data = validated_data.pop("personal_data")
        social_media_data = validated_data.pop("social_media_data")

        if "child" not in validated_data or validated_data["child"] is None or validated_data["child"] == "":
            child = Child.objects.create()
            validated_data["child"] = child

        case = Case.objects.create(**validated_data)

        PhysicalData.objects.create(case=case, **physical_data)

        personal_data["full_name"] = "{} {}".format(personal_data["first_name"], personal_data["last_name"])
        PersonalData.objects.create(case=case, **personal_data)
        PsychologicalData.objects.create(case=case, **psychological_data)
        MedicalData.objects.create(case=case, **medical_data)
        DemographicData.objects.create(case=case, **demographic_data)
        SocialMediaData.objects.create(case=case, **social_media_data)
        return case


class CaseSerializer(serializers.ModelSerializer):

    demographic_data = DemographicDataSerializer()
    medical_data = MedicalDataSerializer()
    psychological_data = PsychologicalDataSerializer()
    physical_data = PhysicalDataSerializer()
    personal_data = PersonalDataSerializer()
    social_media_data = SocialMediaDataSerializer()
    disappearance_date = serializers.SerializerMethodField(read_only=True)
    disappearance_location = serializers.SerializerMethodField(read_only=True)
    age = serializers.SerializerMethodField()
    arrival_date = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    nationality = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    medical_treatment_required = serializers.SerializerMethodField()
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
            return current_facility.name
        except Facility.DoesNotExist:
            return None

    def get_nationality(self, case):
        return case.demographic_data.nationality

    def get_medical_treatment_required(self, case):
        return case.medical_data.medical_treatment_required

    def get_gender(self, case):
        return case.demographic_data.gender

    def get_arrival_date(self, case):
        return case.demographic_data.arrival_at_facility_date

    def get_first_name(self, case):
        return case.personal_data.first_name

    def get_last_name(self, case):
        return case.personal_data.last_name

    def get_age(self, case):
        return case.demographic_data.date_of_birth

    def get_disappearance_date(self, case):
        feedbacks = Feedback.objects.filter(case=case).order_by("id")
        if case is not None and feedbacks is not None and len(feedbacks) > 0:
            return feedbacks[0].date
        else:
            return ""

    def get_disappearance_location(self, case):
        feedbacks = Feedback.objects.filter(case=case).order_by("date")
        if case is not None and feedbacks is not None and len(feedbacks) > 0:
            return feedbacks[0].address
        else:
            return ""

    def update(self, instance, validated_data):
        def handle_demographic_data(data):
            if data is not None:
                demographic_data_instance = DemographicData.objects.get(case=instance)
                serializer = DemographicDataSerializer()
                serializer.update(demographic_data_instance, data)

        def handle_medical_data(data):
            if data is not None:
                medical_data_instance = MedicalData.objects.get(case=instance)
                serializer = MedicalDataSerializer()
                serializer.update(medical_data_instance, data)

        def handle_psychological_data(data):
            if data is not None:
                psychological_data_instance = PsychologicalData.objects.get(case=instance)
                serializer = PsychologicalDataSerializer()
                serializer.update(psychological_data_instance, data)

        def handle_physical_data(data):
            if data is not None:
                physical_data_instance = PhysicalData.objects.get(case=instance)
                serializer = PhysicalDataSerializer()
                serializer.update(physical_data_instance, data)

        def handle_personal_data(data):
            if data is not None:
                data["full_name"] = data["last_name"] + " " + data["first_name"]
                personal_data_instance = PersonalData.objects.get(case=instance)
                serializer = PersonalDataSerializer()
                serializer.update(personal_data_instance, data)

        def handle_social_media_data(data):
            if data is not None:
                social_media_data_instance = SocialMediaData.objects.get(case=instance)
                serializer = SocialMediaDataSerializer()
                serializer.update(social_media_data_instance, data)

        demographic_data = validated_data.pop("demographic_data")
        medical_data = validated_data.pop("medical_data")
        psychological_data = validated_data.pop("psychological_data")
        physical_data = validated_data.pop("physical_data")
        personal_data = validated_data.pop("personal_data")
        social_media_data = validated_data.pop("social_media_data")

        serializers.ModelSerializer.update(self, instance, validated_data)

        handle_demographic_data(demographic_data)
        handle_medical_data(medical_data)
        handle_psychological_data(psychological_data)
        handle_physical_data(physical_data)
        handle_personal_data(personal_data)
        handle_social_media_data(social_media_data)

        return instance
