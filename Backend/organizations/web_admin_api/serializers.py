from django.shortcuts import get_object_or_404
from rest_framework import serializers

from facilities.models import Facility
from organizations.models import Organization
from users.models import User


class OrganizationSerializer(serializers.ModelSerializer):
    # logo = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = "__all__"

    # def get_logo(self, instance):
    #     if not instance.logo:
    #         return None
    #     request = self.context.get("request")
    #     return request.build_absolute_uri(instance.logo.url)


class OrganizationUsersSerializer(serializers.ModelSerializer):
    facility_name = serializers.SerializerMethodField()
    is_hosting_facility = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    @staticmethod
    def get_facility_name(user):
        return user.facility.name if user.facility else ""

    @staticmethod
    def get_is_hosting_facility(user):
        return user.facility.supports_hosting if user.facility else None
