import analytics.analytics_case as ac

from rest_framework import serializers

from cases.models import (
    Case,
    SocialMedia,
    Child,
    FacilityHistory,
    CaseVolunteer,
    File,
    Feed,
    CaseVolunteerLocation,
    SocialNetworksData,
)
from facilities.models import Facility
from feedbacks.models import Feedback


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = "__all__"


class SocialNetworksDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetworksData
        fields = "__all__"


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"


class SimilarCasesSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = "__all__"

    @staticmethod
    def get_first_name(case):
        return case.child.first_name

    @staticmethod
    def get_last_name(case):
        return case.child.last_name


class CasesSerializer(serializers.ModelSerializer):

    disappearance_date = serializers.SerializerMethodField(read_only=True)
    disappearance_location = serializers.SerializerMethodField(read_only=True)
    arrival_date = serializers.SerializerMethodField()
    # profile_photo = serializers.SerializerMethodField()

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

    # def get_profile_photo(self, instance):
    #     if not instance.profile_photo:
    #         return None
    #     request = self.context.get("request")
    #     return request.build_absolute_uri(instance.profile_photo.url)

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

    # def create(self, validated_data):
    #     case = Case.objects.create(**validated_data)
    #     ceng = ac.ProfileEvalEngine(case)
    #     data = ceng.get_profiling_preds_json()
    #     case.data = data
    #     case.save()
    #     return case

    def update(self, instance, validated_data):
        serializers.ModelSerializer.update(self, instance, validated_data)
        ceng = ac.ProfileEvalEngine(instance)
        data = ceng.get_profiling_preds_json()
        instance.data = data
        instance.save()
        return instance

    # def create(self, validated_data):
    #     social_media_data = validated_data.pop("social_media_data")
    #     case = Case.objects.create(**validated_data)
    #     SocialMediaData.objects.create(case=case, **social_media_data)
    #     return case
    #
    # def update(self, instance, validated_data):
    #     def handle_social_media_data(data):
    #         if data is not None:
    #             social_media_data_instance = SocialMediaData.objects.get(case=instance)
    #             serializer = SocialMediaDataSerializer()
    #             serializer.update(social_media_data_instance, data)
    #
    #     social_media_data = validated_data.pop("social_media_data")
    #     serializers.ModelSerializer.update(self, instance, validated_data)
    #     handle_social_media_data(social_media_data)
    #     return instance


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
