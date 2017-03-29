from django.shortcuts import render

from django.http import HttpResponse
from rest_framework import viewsets
from report.serializers import *
from report.models import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from datetime import date


class ReportToday(APIView):

    def get(self, request, format=None):
        unit_id = request.GET.get('unit')
        if unit_id is None or not unit_id.isdigit():
            return Response('Enter unit number like \'unit=818\'', status=status.HTTP_400_BAD_REQUEST)

        chosen_unit = Unit.objects.all().filter(id=unit_id)
        if chosen_unit is None or len(chosen_unit) < 1:
            return Response('No such unit exist', status=status.HTTP_400_BAD_REQUEST)
        chosen_unit = chosen_unit[0]

        single_report = Report.objects.all().filter(unit=unit_id).filter(date=date.today())
        if len(single_report) == 0:
            # if no report for today is made yet, making one, and adding all relevant people with NOT_SET status.
            single_report = [Report.objects.create(date=date.today(), unit=chosen_unit)]
            single_report = single_report[0]
            persons = Person.objects.all().filter(unit_id=unit_id)
            for person in persons:
                ReportEntry.objects.create(person=person, status='NOT_SET', report=single_report)
        else:
            single_report = single_report[0]
        serializer = ReportSerializer(single_report)
        return Response(serializer.data)


class ReportList(APIView):

    def get(self, request, format=None):
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        report = self.get_object(pk)
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        report = self.get_object(pk)
        serializer = ReportSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        report = self.get_object(pk)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportEntryList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        report_entries = ReportEntry.objects.all()
        serializer = ReportEntryGetSerializer(report_entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReportEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportEntryDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return ReportEntry.objects.get(pk=pk)
        except ReportEntry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        report_entry = self.get_object(pk)
        serializer = ReportEntrySerializer(report_entry)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        report_entry = self.get_object(pk)
        serializer = ReportEntrySerializer(report_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        report_entry = self.get_object(pk)
        report_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)