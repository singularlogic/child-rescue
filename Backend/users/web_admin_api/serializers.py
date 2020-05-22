from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from facilities.models import Facility
from organizations.models import Organization
from users.models import User


# class OrganizationListingField(serializers.RelatedField):
#     def to_representation(self, instance):
#         return instance.id
#
#     def to_internal_value(self, data):
#         return get_object_or_404(Organization, id=data)
#
#     def get_queryset(self):
#         return Organization.objects.all()
#
#
# class FacilityListingField(serializers.RelatedField):
#     def to_representation(self, instance):
#         return instance.id
#
#     def to_internal_value(self, data):
#         return get_object_or_404(Facility, id=data)
#
#     def get_queryset(self):
#         return Facility.objects.all()

#
# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     organization = OrganizationListingField(required=False)
#     facility = FacilityListingField(required=False)
#     facility_name = serializers.SerializerMethodField(read_only=True)
#
#     def create(self, validated_data):
#         role = validated_data["role"]
#         organization = validated_data.get("organization", None)
#         facility = validated_data.get("facility", None)
#         first_name = validated_data.get("first_name", None).lower()
#         last_name = validated_data.get("last_name", None).lower()
#         # is_team_leader = validated_data.get("is_team_leader", None)
#
#         if role not in ['simple_user', 'volunteer'] and (organization is None or facility is None):
#             raise ValidationError({'detail': 'Must provide organization and facility for {}'.format(role)})
#
#         if role == 'volunteer' and organization is None:
#             raise ValidationError({'detail': 'Must provide organization for {}'.format(role)})
#         if role != 'simple_user' and (first_name is None or last_name is None):
#             raise ValidationError({'detail': 'Must provide first and last name for {}'.format(role)})
#
#         user = self.context['request'].user
#         if user.role == 'organization_manager':
#             if user.organization != organization:
#                 raise ValidationError({'detail': 'Organization manager can only add users to its own organization'})
#
#         if role != 'volunteer':
#             # is_team_leader = None
#             if facility.organization != organization:
#                 raise ValidationError({'detail': 'Facility belongs to different organization'})
#         else:
#             facility = None
#
#         if role == 'simple_user':
#             organization = None
#             facility = None
#             # is_team_leader = None
#
#         new_user = User.objects.create(
#             organization=organization,
#             facility=facility,
#             role=role,
#             email=validated_data["email"].lower(),
#             first_name=first_name,
#             last_name=last_name,
#             # is_team_leader=is_team_leader,
#             phone=validated_data.get("phone", None),
#             address=validated_data.get("address", None),
#             latitude=validated_data.get("latitude", None),
#             longitude=validated_data.get("longitude", None),
#             description=validated_data.get("description", None),
#             is_end_user=True,
#             is_active=True,
#         )
#         new_user.set_password(validated_data["password"])
#         new_user.save()
#         return new_user
#
#     class Meta:
#         model = User
#         fields = "__all__"
#
#     @staticmethod
#     def get_facility_name(user):
#         from facilities.models import Facility
#         try:
#             if user.facility:
#                 facility = Facility.objects.get(id=user.facility.id)
#                 return facility.name
#             return ""
#         except Facility.DoesNotExist:
#             return ""


class UserSerializer(serializers.ModelSerializer):
    facility_name = serializers.SerializerMethodField()
    is_hosting_facility = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"].lower(),
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data["role"],
            organization=validated_data["organization"],
            facility=validated_data["facility"],
            address=validated_data["address"] if "address" in validated_data else None,
            city=validated_data["city"] if "city" in validated_data else None,
            latitude=validated_data["latitude"] if "latitude" in validated_data else None,
            longitude=validated_data["longitude"] if "longitude" in validated_data else None,
            phone=validated_data["phone"] if "phone" in validated_data else None,
            description=validated_data["description"] if "description" in validated_data else None,
            is_end_user=True,
            is_active=True,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = "__all__"

    @staticmethod
    def get_facility_name(user):
        return user.facility.name if user.facility else ""

    @staticmethod
    def get_is_hosting_facility(user):
        return user.facility.supports_hosting if user.facility else None


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    uid = serializers.CharField(write_only=True)
