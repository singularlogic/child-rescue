from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from core.cases.models import DemographicData, MedicalData, SocialData, PhysicalData, ProfileData, Case


class DemographicDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)
    child = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DemographicData
        fields = '__all__'

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child


class MedicalDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)
    child = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MedicalData
        fields = '__all__'

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child


class SocialDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)
    child = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SocialData
        fields = '__all__'

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child


class PhysicalDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)
    child = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PhysicalData
        fields = '__all__'

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child


class ProfileDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)
    child = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProfileData
        fields = '__all__'

    @staticmethod
    def get_case(instance):
        return instance.case.id

    @staticmethod
    def get_child(instance):
        return instance.case.child


class CaseSerializer(serializers.ModelSerializer):

    demographic_data = DemographicDataSerializer()
    medical_data = MedicalDataSerializer()
    social_data = SocialDataSerializer()
    physical_data = PhysicalDataSerializer()
    profile_data = ProfileDataSerializer()

    class Meta:
        model = Case
        fields = '__all__'

    def create(self, validated_data):

        demographic_data = validated_data.pop('demographic_data')
        medical_data = validated_data.pop('medical_data')
        social_data = validated_data.pop('social_data')
        physical_data = validated_data.pop('physical_data')
        profile_data = validated_data.pop('profile_data')

        case = Case.objects.create(**validated_data)

        PhysicalData.objects.create(case=case, child=case.child, **physical_data)
        ProfileData.objects.create(case=case, child=case.child, **profile_data)
        SocialData.objects.create(case=case, child=case.child, **social_data)
        MedicalData.objects.create(case=case, child=case.child, **medical_data)
        DemographicData.objects.create(case=case, child=case.child, **demographic_data)

        return case

    def update(self, instance, validated_data):

        def handle_demographic_data(data):
            if data is not None:
                demographic_data_instance = DemographicData.objects.get(case=instance, child=instance.child)
                serializer = DemographicDataSerializer()
                serializer.update(demographic_data_instance, data)

        def handle_medical_data(data):
            if data is not None:
                medical_data_instance = MedicalData.objects.get(case=instance, child=instance.child)
                serializer = MedicalDataSerializer()
                serializer.update(medical_data_instance, data)

        def handle_social_data(data):
            if data is not None:
                social_data_instance = SocialData.objects.get(case=instance, child=instance.child)
                serializer = SocialDataSerializer()
                serializer.update(social_data_instance, data)

        def handle_physical_data(data):
            if data is not None:
                physical_data_instance = PhysicalData.objects.get(case=instance, child=instance.child)
                serializer = PhysicalDataSerializer()
                serializer.update(physical_data_instance, data)

        def handle_profile_data(data):
            if data is not None:
                profile_data_instance = ProfileData.objects.get(case=instance, child=instance.child)
                serializer = ProfileDataSerializer()
                serializer.update(profile_data_instance, data)

        demographic_data = validated_data.pop('demographic_data')
        medical_data = validated_data.pop('medical_data')
        social_data = validated_data.pop('social_data')
        physical_data = validated_data.pop('physical_data')
        profile_data = validated_data.pop('profile_data')

        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        handle_demographic_data(demographic_data)
        handle_medical_data(medical_data)
        handle_social_data(social_data)
        handle_physical_data(physical_data)
        handle_profile_data(profile_data)

        return instance
