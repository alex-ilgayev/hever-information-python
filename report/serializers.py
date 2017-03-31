from .models import *
from rest_framework import serializers


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ('id', 'name')

    def create(self, validated_data):
        return Unit.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date = validated_data.get('name', instance.date)
        instance.save()
        return instance


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'description', 'unit')

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date = validated_data.get('first_name', instance.date)
        instance.date = validated_data.get('last_name', instance.date)
        instance.date = validated_data.get('description', instance.date)
        instance.save()
        return instance

# A serializer class only for get requests.
# contains detail for person.
class ReportEntryGetSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)

    class Meta:
        model = ReportEntry
        fields = ('id', 'status', 'report', 'person')

# A serializer class for all other responses.
# contain person as foreign key.
class ReportEntryUpdateSerializer(serializers.ModelSerializer):

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
    report_entries = ReportEntryGetSerializer(many=True)
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ('id', 'date', 'unit', 'report_entries')

    def create(self, validated_data):
        return Report.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance
