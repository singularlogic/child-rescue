from rest_framework import serializers

from core.users.models import User, UuidActivity


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'].lower(),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_end_user=validated_data['is_end_user'],
            is_active=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'profile_image', 'is_end_user')


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)


class UuidActivitySerializer(serializers.ModelSerializer):
    uuid = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UuidActivity
        fields = '__all__'
