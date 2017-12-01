from .models import *
from rest_framework import serializers


class GeoReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeoReport
        fields = ('id', 'long', 'lat', 'timestamp')

    def create(self, validated_data):
        return GeoReport.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.long = validated_data('long', instance.long)
        instance.lat = validated_data('lat', instance.lat)
        instance.timestamp = validated_data('timestamp', instance.timestamp)
        instance.save()
        return instance
