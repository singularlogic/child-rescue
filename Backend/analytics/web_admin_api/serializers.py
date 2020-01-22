from rest_framework import serializers


class CountItemSerializer(serializers.Serializer):
    date_field = serializers.DateField(read_only=True)
    count = serializers.IntegerField(read_only=True)


class AreaSerializer(serializers.Serializer):
    date = serializers.DateField(read_only=True)
    area = serializers.FloatField(read_only=True)


class CountSerializer(serializers.Serializer):
    counts = CountItemSerializer(read_only=True, many=True)
    average = serializers.FloatField(read_only=True)
