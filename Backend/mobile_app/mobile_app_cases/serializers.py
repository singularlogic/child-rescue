from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from core.cases.models import DemographicData, MedicalData, SocialData, PhysicalData, ProfileData, Case
from core.cases.utils import CaseUtils


class DemographicDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemographicData
        fields = '__all__'


class MedicalDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalData
        fields = '__all__'


class SocialDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialData
        fields = '__all__'


class PhysicalDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhysicalData
        fields = '__all__'


class ProfileDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileData
        fields = '__all__'


class CaseSerializer(serializers.ModelSerializer):

    demographic_data = serializers.SerializerMethodField()
    medical_data = serializers.SerializerMethodField()
    social_data = serializers.SerializerMethodField()
    physical_data = serializers.SerializerMethodField()
    profile_data = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = '__all__'

    @staticmethod
    def get_demographic_data(case):
        return DemographicDataSerializer(CaseUtils.get_demographic_data(case.child, case.id)).data

    @staticmethod
    def get_medical_data(case):
        return MedicalDataSerializer(CaseUtils.get_medical_data(case.child, case.id)).data

    @staticmethod
    def get_social_data(case):
        return SocialDataSerializer(CaseUtils.get_social_data(case.child, case.id)).data

    @staticmethod
    def get_physical_data(case):
        return PhysicalDataSerializer(CaseUtils.get_medical_data(case.child, case.id)).data

    @staticmethod
    def get_profile_data(case):
        return ProfileDataSerializer(CaseUtils.get_medical_data(case.child, case.id)).data

    def create(self, validated_data):

        def handle_demographic_data(data):
            if data is not None:
                data['case'] = case.id
                data['child'] = validated_data['child'].id

                serializer = DemographicDataSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                data = DemographicData(child=validated_data['child'], case=case)
                data.save()

        def handle_medical_data(data):
            if data is not None:
                data['case'] = case.id
                data['child'] = validated_data['child'].id

                serializer = MedicalDataSerializer(data=data)
                serializer.is_valid()
                serializer.save()
            else:
                data = MedicalData(child=validated_data['child'], case=case)
                data.save()

        def handle_social_data(data):
            if data is not None:
                data['case'] = case.id
                data['child'] = validated_data['child'].id

                serializer = SocialDataSerializer(data=data)
                serializer.is_valid()
                serializer.save()
            else:
                data = SocialData(child=validated_data['child'], case=case)
                data.save()

        def handle_physical_data(data):
            if data is not None:
                data['case'] = case.id
                data['child'] = validated_data['child'].id

                serializer = PhysicalDataSerializer(data=data)
                serializer.is_valid()
                serializer.save()
            else:
                data = PhysicalData(child=validated_data['child'], case=case)
                data.save()

        def handle_profile_data(data):
            if data is not None:
                data['case'] = case.id
                data['child'] = validated_data['child'].id

                serializer = ProfileDataSerializer(data=data)
                serializer.is_valid()
                serializer.save()
            else:
                data = ProfileData(child=validated_data['child'], case=case)
                data.save()

        demographic_data = validated_data.pop('demographic_data')
        medical_data = validated_data.pop('medical_data')
        social_data = validated_data.pop('social_data')
        physical_data = validated_data.pop('physical_data')
        profile_data = validated_data.pop('profile_data')

        case = Case.objects.create(**validated_data)

        handle_demographic_data(demographic_data)
        handle_medical_data(medical_data)
        handle_social_data(social_data)
        handle_physical_data(physical_data)
        handle_profile_data(profile_data)

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
