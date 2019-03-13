from rest_framework import serializers

from core.evidences.models import Evidence


class EvidenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evidence
        fields = '__all__'
