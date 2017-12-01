from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from hever_information.settings import DATE
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login
from oauth2client.crypt import AppIdentityError
from oauth2client.client import verify_id_token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from django.db import *
from geo_report.serializers import *
import json

import re

class GeoReportList(APIView):

    #receiving date in parameters.
    def get(self, request):

        chosen_date = request.GET.get(DATE)
        geo_reports_returned = GeoReport.objects.all()

        # checking validity of parameters
        if chosen_date is not None:
            re_result = re.search('([0-9]{2})-([0-9]{2})-([0-9]{4})', chosen_date)
            if re_result is None:
                return Response('Wrong date format. enter date format like: date=05-06-1970'
                                , status=status.HTTP_400_BAD_REQUEST)
            day = re_result.group(1)
            month = re_result.group(2)
            year = re_result.group(3)

            if day is None or month is None or year is None:
                return Response('Wrong date format. enter date format like: date=05-06-1970'
                                , status=status.HTTP_400_BAD_REQUEST)

            day = int(day)
            month = int(month)
            year = int(year)

            if day is None or month is None or year is None:
                return Response('Wrong date format. enter date format like: date=05-06-1970'
                                , status=status.HTTP_400_BAD_REQUEST)

            chosen_datetime = datetime(year=year, month=month, day=day)

            chosen_datetime = chosen_datetime.strftime('%Y-%m-%d')
            geo_reports_returned = geo_reports_returned.filter(timestamp__gt=chosen_datetime)

        serializer = GeoReportSerializer(geo_reports_returned, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GeoReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ReportDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Report.objects.get(pk=pk)
#         except Report.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         geo_report = self.get_object(pk)
#         serializer = ReportSerializer(geo_report)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         geo_report = self.get_object(pk)
#         serializer = ReportSerializer(geo_report, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         geo_report = self.get_object(pk)
#         geo_report.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ReportEntryList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         report_entries = ReportEntry.objects.all()
#         serializer = ReportEntryGetSerializer(report_entries, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ReportEntrySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportEntryDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return ReportEntry.objects.get(pk=pk)
        except ReportEntry.DoesNotExist:
            raise Http404
    #
    # def get(self, request, pk, format=None):
    #     report_entry = self.get_object(pk)
    #     serializer = ReportEntryUpdateSerializer(report_entry)
    #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        # is response None, everything good. else return tuple (text, response status)
        response_val = authenticate_google_token_id(request)

        if response_val is not None:
            return Response(response_val[0], status=response_val[1])

        report_entry = self.get_object(pk)

        # check permission to update.
        if not request.user.has_perm('geo_report.can_update_unit_' + str(report_entry.report.unit_id)):
            return Response('no permission for doing the operation', status=status.HTTP_403_FORBIDDEN)

        serializer = ReportEntryUpdateSerializer(report_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     report_entry = self.get_object(pk)
    #     report_entry.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class UnitList(APIView):

    def get(self, request, format=None):
        # is response None, everything good. else return tuple (text, response status)
        response_val = authenticate_google_token_id(request)

        if response_val is not None:
            return Response(response_val[0], status=response_val[1])

        units_returned = Unit.objects.all()
        serializer = UnitSerializer(units_returned, many=True)
        return Response(serializer.data)


# receives request for service, check validity of the google token id,
# and login to the appropriate user (if not exist, creates it.
# returns tuple of (message response, status response)
# if None then success.
def authenticate_google_token_id(request):
    google_token_id = request.GET.get(GOOGLE_TOKEN_ID)
    if google_token_id is None:
        return ('no token is provided', status.HTTP_403_FORBIDDEN)

    # Update client_secrets.json with your Google API project information.
    # Do not change this assignment.
    CLIENT_ID = json.loads(
        open('client_secret.json', 'r').read())['web']['client_id']

    try:
        # Client library can verify the ID token.
        jwt = verify_id_token(google_token_id, CLIENT_ID)
        gid = jwt['sub']
        email = jwt['email']

    # failed authentication with google
    except AppIdentityError:
        return ('google token id provided is invalid', status.HTTP_403_FORBIDDEN)

    # checks if user exists. if not, then creates.
    exists = User.objects.all().filter(username=email).exists()
    if not exists:
        try:
            user = User.objects.create_user(email, password=CONSTANT_PASSWORD)
            user.save()
        except IntegrityError:
            # shouldn't happen
            return ('user creation error', status.HTTP_500_INTERNAL_SERVER_ERROR)
            # user is created now.

    # up to now validated google token id. now logs in using django auth system.
    user = authenticate(username=email, password=CONSTANT_PASSWORD)

    # shouldn't happen
    if user is None:
        return ('login error', status.HTTP_500_INTERNAL_SERVER_ERROR)

    login(request, user=user)
    return None
