import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from compliance.models import DataLogEntry
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from dj_rest_auth.views import LoginView as RestAuthBaseLoginView
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from django.conf import settings
from lists.models import ListEntry
from domains.models import Domain
from mail.models import SmtpRelay
from pymailq.store import PostqueueStore
import pyotp
import csv
import os
import shutil
from io import StringIO
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
import urllib
import geoip2.database
from pathlib import Path
from core.helpers import which
import psutil

class CurrentUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    def get_permissions(self):
        return (IsAuthenticated()),

class DataImportUploadAPIView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request):
        print(request.data)
        import_file = request.data.get('file', False)
        if not import_file:
            return Response({
                'non_field_errors': [_('The request did not provide a file to process')]
            }, status=status.HTTP_400_BAD_REQUEST)
        import_file.seek(0)
        datareader = csv.reader(StringIO(import_file.read().decode()), delimiter=';', quotechar='"')
        model = False
        for row in datareader:
            if request.data.get('import_type', False) == 'list_entry':
                from_address = row[0]
                from_domain = row[0].split('@')[1]
                to_address = row[1]
                to_domain = row[1].split('@')[1]
                ListEntry.objects.create(**{
                    'from_address': from_address,
                    'from_domain': from_domain,
                    'to_address': to_address,
                    'to_domain': to_domain,
                    'listing_type': row[2]
                })
            elif request.data.get('import_type', False) == 'domain':
                Domain.objects.create(**{
                    'name': row[0],
                    'destination': row[1],
                    'receive_type': row[2],
                    'active': row[3],
                    'allowed_accounts': row[4]
                })
            elif request.data.get('smtp_relay', False) == 'smtp_relay':
                SmtpRelay.objects.create(**{
                    'ip_address': row[0],
                    'hostname': row[1],
                    'active': row[2],
                    'comment': row[3]
                })
        return Response({}, status=status.HTTP_200_OK)

class GeoIPLookupAPIView(APIView):
    def post(self, request):
        country = False
        if not request.data.get('ip_addr', False):
            return Response({
                'non_field_errors': [_('No IP address was provided')]
            }, status=status.HTTP_400_BAD_REQUEST)
        if not settings.MAXMIND_ACCOUNT_API_KEY:
            return Response({
                'non_field_errors': [_('MaxMind GeoIP configuration is not complete')]
            }, status=status.HTTP_400_BAD_REQUEST)
        if not settings.MAXMIND_DB_FILE.exists():
            return Response({
                'No GeoLite2 database exists on the system'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        with geoip2.database.Reader(settings.MAXMIND_DB_FILE) as geoip:
            result = geoip.country(request.data.get('ip_addr'))
            country = result.country.name or False

        if not country:
            return Response({
                'non_field_errors': [
                    'No country was found matching IP {}'.format(request.data.get('ip_addr'))
                ]
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({ 'country':country }, status=status.HTTP_200_OK)

class GeoIPUpdateAPIView(APIView):
    def get(self, request):
        if not all([settings.MAXMIND_ACCOUNT_API_KEY, settings.MAXMIND_DB_PATH, settings.MAXMIND_DB_FILE]):
            return Response({
                'non_field_errors': ['MaxMind Database configuration is incomplete']
            }, status=status.HTTP_400_BAD_REQUEST)
        filepath, headers = urllib.request.urlretrieve('https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key={key}&suffix=tar.gz'.format(key=settings.MAXMIND_ACCOUNT_API_KEY))
        subprocess.call([which('tar'), 'xvzf {} -C {}'.format(filepath, settings.MAXMIND_DB_PATH)])
        for path in os.listdir(settings.MAXMIND_DB_PATH):
            if path[:16] == 'GeoLite2-Country':
                if Path(settings.MAXMIND_DB_PATH, path, 'GeoLite2-Country.mmdb').exists():
                    Path(settings.MAXMIND_DB_PATH, 'GeoLite2-Country.mmdb').rename(settings.MAXMIND_DB_FILE)
                    shutil.rmtree(Path(settings.MAXMIND_DB_PATH, path))
        DataLogEntry.objects.log_create(request.user, changes='User {} has performed an update of the MaxMind GeoLite2 database'.format(request.user.email))
        return Response({}, status=status.HTTP_200_OK)

class SystemMetricsAPIView(APIView):
    def get(self, request):
        data = {
            'hostname': 'localhost',
            'cpu_load': psutil.cpu_percent(3),
            'ram_usage': psutil.virtual_memory()[2]
        }
        if which('mailq'):
            store = PostqueueStore()
            store.load()
            data['queue'] = store.mails.count()
        return Response(data, status=status.HTTP_200_OK)