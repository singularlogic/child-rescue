from rest_framework import serializers

from .models import Case, Child, Profile


class ChildSerializer(serializers.ModelSerializer):
    cases = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all(), many=True)

    class Meta:
        model = Child
        fields = '__all__'


class CaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        fields = ('id', 'is_active', 'child_id')


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

