from rest_framework import serializers

from places.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Place
        fields = "__all__"

    @staticmethod
    def get_image(place):
        if place.feedback is not None:
            return str(place.feedback.feedback_image)
        else:
            return ""
