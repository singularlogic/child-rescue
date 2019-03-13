from rest_framework import serializers

from core.choices.models import SchoolGrades


class SchoolGradesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolGrades
        fields = '__all__'
