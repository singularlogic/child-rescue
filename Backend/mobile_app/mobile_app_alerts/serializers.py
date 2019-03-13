from rest_framework import serializers

from core.alerts.models import Alert


class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = '__all__'
