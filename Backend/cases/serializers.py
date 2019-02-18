from rest_framework import serializers

from .models import Case, Child, Profile, Physical, Social, Medical, Demographics


class ChildSerializer(serializers.ModelSerializer):
    cases = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all(), many=True)

    class Meta:
        model = Child
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    case_id = serializers.SerializerMethodField()
    case_is_active = serializers.SerializerMethodField()
    child_id = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'child_id', 'case_id', 'case_is_active')

    @staticmethod
    def get_case_id(instance):
        return instance.case.id

    @staticmethod
    def get_case_is_active(instance):
        return instance.case.is_active

    @staticmethod
    def get_child_id(instance):
        return instance.case.child_id


class PhysicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Physical
        fields = ('id', 'height', 'weight')


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ('id', 'social_media')


class MedicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical
        fields = ('id', 'health_issues', 'medical_treatment_required')


class DemographicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demographics
        fields = ('id', 'home_address')


class CaseSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=False)
    physicals = PhysicalSerializer(many=False)
    socials = SocialSerializer(many=False)
    medicals = MedicalSerializer(many=False)
    demographics = DemographicsSerializer(many=False)

    class Meta:
        model = Case
        fields = ('id', 'is_active', 'child_id', 'profiles', 'physicals', 'socials', 'medicals', 'demographics')

    def create(self, validated_data):

        profiles = validated_data.pop('profiles')
        physicals = validated_data.pop('physicals')
        socials = validated_data.pop('socials')
        medicals = validated_data.pop('medicals')
        demographics = validated_data.pop('demographics')
        case = Case.objects.create(**validated_data)

        Physical.objects.create(case=case, **physicals)
        Profile.objects.create(case=case, **profiles)
        Social.objects.create(case=case, **socials)
        Medical.objects.create(case=case, **medicals)
        Demographics.objects.create(case=case, **demographics)

        return case




