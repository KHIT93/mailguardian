import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from .models import MailScannerConfiguration, User, TwoFactorConfiguration, TwoFactorBackupCode
from compliance.models import DataLogEntry
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_auth.views import LoginView as RestAuthBaseLoginView
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from django.conf import settings
from .exceptions import TwoFactorRequired, TwoFactorInvalid, InvalidBackupCode
from rest_auth.app_settings import create_token, JWTSerializer
from rest_auth.utils import jwt_encode
from .helpers import TOTP
from lists.models import ListEntry
from domains.models import Domain
from mail.models import SmtpRelay
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

class MailScannerConfigurationFilePathsView(APIView):
    def get(self, request):
        files = MailScannerConfiguration.objects.values('filepath').distinct()
        return Response(files)
    
    def get_permissions(self):
        return (IsAdminUser()),

class LoginView(RestAuthBaseLoginView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data, context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        try:
            self.login()
        except TwoFactorRequired as e:
            return Response({
                'two_factor_token': [_('Please provide your two factor login code')]
            }, status=status.HTTP_400_BAD_REQUEST)
        except TwoFactorInvalid as e:
            return Response({
                'non_field_errors': [_('The provided 2FA code is invalid')],
                'two_factor_token': [_('Please provide your two factor login code')]
            }, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidBackupCode as e:
            return Response({
                'non_field_errors': [_('The provided backup code is invalid')],
                'backup_code': [_('The provided backup code is invalid')]
            }, status=status.HTTP_401_UNAUTHORIZED)

        return self.get_response()


    def login(self):
        self.user = self.serializer.validated_data['user']

        if self.user.get_has_two_factor():
            # Check if we have a backup code in request.data
            if 'backup_code' in self.serializer.validated_data and self.serializer.validated_data['backup_code'] != '' and not self.serializer.validated_data['backup_code'] is None:
                match_code = None
                codes = TwoFactorBackupCode.objects.filter(user=self.user)
                for code in codes:
                    if self.serializer.validated_data['backup_code'] == code.code:
                        match_code = code
                if not match_code:
                    raise InvalidBackupCode()
                else:
                    match_code.delete()
            # Verify 2FA code
            elif self.serializer.validated_data['two_factor_token'] != '' and not self.serializer.validated_data['two_factor_token'] is None:
                totp = TOTP(TwoFactorConfiguration.objects.get(user=self.user).totp_key)
                print(self.serializer.validated_data['two_factor_token'])
                print(totp.now())
                if not totp.verify(self.serializer.validated_data['two_factor_token']):
                    raise TwoFactorInvalid()
            # Raise Exception if code is not valid
            else:
                raise TwoFactorRequired()

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

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
