from rest_framework import serializers

from core.cases.models import DemographicData, MedicalData, PsychologicalData, PhysicalData, PersonalData, Case, SocialMediaData


class DemographicDataSerializer(serializers.ModelSerializer):

    case = serializers.PrimaryKeyRelatedField(read_only=True)

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

    class Meta:
        model = MedicalData
        fields = '__all__'

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
        fields = '__all__'

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
        fields = '__all__'

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
        fields = '__all__'

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
    psychological_data = PsychologicalDataSerializer()
    physical_data = PhysicalDataSerializer()
    personal_data = PersonalDataSerializer()
    social_media_data = SocialMediaDataSerializer()

    class Meta:
        model = Case
        fields = '__all__'

    def create(self, validated_data):

        demographic_data = validated_data.pop('demographic_data')
        medical_data = validated_data.pop('medical_data')
        psychological_data = validated_data.pop('psychological_data')
        physical_data = validated_data.pop('physical_data')
        personal_data = validated_data.pop('personal_data')
        social_media_data = validated_data.pop('social_media_data')

        case = Case.objects.create(**validated_data)

        PhysicalData.objects.create(case=case, **physical_data)
        PersonalData.objects.create(case=case, **personal_data)
        PsychologicalData.objects.create(case=case, **psychological_data)
        MedicalData.objects.create(case=case, **medical_data)
        DemographicData.objects.create(case=case, **demographic_data)
        SocialMediaData.objects.create(case=case, **social_media_data)

        return case

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
                personal_data_instance = PersonalData.objects.get(case=instance)
                serializer = PersonalDataSerializer()
                serializer.update(personal_data_instance, data)

        def handle_social_media_data(data):
            if data is not None:
                social_media_data_instance = SocialMediaData.objects.get(case=instance)
                serializer = SocialMediaDataSerializer()
                serializer.update(social_media_data_instance, data)

        demographic_data = validated_data.pop('demographic_data')
        medical_data = validated_data.pop('medical_data')
        psychological_data = validated_data.pop('psychological_data')
        physical_data = validated_data.pop('physical_data')
        personal_data = validated_data.pop('personal_data')
        social_media_data = validated_data.pop('social_media_data')

        serializers.ModelSerializer.update(self, instance, validated_data)

        handle_demographic_data(demographic_data)
        handle_medical_data(medical_data)
        handle_psychological_data(psychological_data)
        handle_physical_data(physical_data)
        handle_personal_data(personal_data)
        handle_social_media_data(social_media_data)

        return instance
