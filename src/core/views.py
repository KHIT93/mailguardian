from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from .models import MailScannerConfiguration, User, TwoFactorConfiguration, TwoFactorBackupCode
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_auth.views import LoginView as RestAuthBaseLoginView
from rest_framework import status
from django.conf import settings
from .exceptions import TwoFactorRequired, TwoFactorInvalid, InvalidBackupCode
from rest_auth.app_settings import create_token, JWTSerializer
from rest_auth.utils import jwt_encode
from .helpers import TOTP
import pyotp
from django.core.exceptions import ObjectDoesNotExist

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
                'two_factor_token': ['Please provide your two factor login code']
            }, status=status.HTTP_400_BAD_REQUEST)
        except TwoFactorInvalid as e:
            return Response({
                'non_field_errors': ['The provided 2FA code is invalid'],
                'two_factor_token': ['Please provide your two factor login code']
            }, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidBackupCode as e:
            return Response({
                'non_field_errors': ['The provided backup code is invalid'],
                'backup_code': ['The provided backup code is invalid']
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