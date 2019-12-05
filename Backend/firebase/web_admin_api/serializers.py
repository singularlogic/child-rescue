from rest_framework import serializers

from firebase.models import FCMDevice


class FCMDeviceSerializer(serializers.ModelSerializer):
    uuid = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FCMDevice
        fields = "__all__"
