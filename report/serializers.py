from .models import *
from rest_framework import serializers


class ReportEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportEntry
        fields = ('id', 'status', 'report', 'person')

    def create(self, validated_data):
        return ReportEntry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class ReportSerializer(serializers.ModelSerializer):
    report_entries = ReportEntrySerializer(many=True)

    class Meta:
        model = Report
        fields = ('id', 'date', 'unit', 'report_entries')

    def create(self, validated_data):
        return Report.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date = validated_data.get('status', instance.date)
        instance.save()
        return instance
