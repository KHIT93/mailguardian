from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import (
    MailScannerConfiguration,
    Setting,
    User,
    MailScannerHost,
    ApplicationTask,
    ApplicationNotification,
    TwoFactorConfiguration,
    TwoFactorBackupCode
)
from .serializers import (
    UserSerializer,
    MailScannerConfigurationSerializer,
    SettingsSerializer,
    ChangePasswordSerializer,
    AuditLogSerializer,
    MailScannerHostSerializer,
    ApplicationTaskSerializer,
    ApplicationNotificationSerializer,
    TwoFactorConfigurationSerialiser,
    TwoFactorBackupCodeSerializer
)
from django.db.models import Q
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from domains.serializers import DomainSerializer
from .permissions import IsDomainAdminOrStaff, IsAdminUserOrReadOnly
from auditlog.models import LogEntry as AuditLog
from rest_framework.permissions import AllowAny
from django.conf import settings
import datetime, pyotp
from django.utils.translation import gettext_lazy as _

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsDomainAdminOrStaff,)
    model = User

    def get_queryset(self):
        qs = super(UserViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return qs
        domains = [domain.name for domain in self.request.user.domains.all()]
        qs = qs.filter(domains__name__in=domains).distinct()
        return qs

    @action(methods=['get'], detail=True, permission_classes=[IsDomainAdminOrStaff], url_path='domains', url_name='user-domains')
    def get_user_domains(self, request, pk=None):
        user = get_object_or_404(User.objects.all(), pk=pk)
        serializer = DomainSerializer(user.domains.all(), many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post'], detail=True, permission_classes=[IsDomainAdminOrStaff], url_path='change-password', url_name='user-change-password')
    def post_user_change_password(self, request, pk=None):
        user = get_object_or_404(User.objects.all(), pk=pk)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not serializer.data.get('new_password1') == serializer.data.get('new_password2'):
                return Response({"new_password1": [_("The passwords do not match.")], "new_password2": [_("The passwords do not match.")]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password1'))
            user.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MailScannerConfigurationViewSet(viewsets.ModelViewSet):
    queryset = MailScannerConfiguration.objects.all()
    serializer_class = MailScannerConfigurationSerializer
    permission_classes = (IsAdminUser,)
    model = MailScannerConfiguration

    def get_queryset(self):
        qs = self.queryset
        if self.request.query_params.__contains__('search'):
            search_key = self.request.query_params.get('search')
            qs = qs.filter(
                    Q(key__icontains=search_key) | Q(value__icontains=search_key)
                )
        if self.request.query_params.__contains__('filename'):
            qs = qs.filter(filepath=self.request.query_params.get('filename'))
        return qs

class SettingsViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingsSerializer
    permission_classes = (IsAdminUser,)
    model = Setting

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated], url_path='by-key', url_name='settings-by-key')
    def post_search_by_key(self, request, pk=None):
        if not 'key' in request.data:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        entity = get_object_or_404(Setting, key=request.data['key'])
        serializer = SettingsSerializer(entity, context={'request': request})
        return Response(serializer.data)

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = (IsAdminUser,)
    model = AuditLog

class MailScannerHostViewSet(viewsets.ModelViewSet):
    queryset = MailScannerHost.objects.all()
    serializer_class = MailScannerHostSerializer
    permission_classes = (IsAdminUser,)
    model = MailScannerHost

class ApplicationTaskViewSet(viewsets.ModelViewSet):
    queryset = ApplicationTask.objects.all()
    serializer_class = ApplicationTaskSerializer
    permission_classes = (IsAuthenticated,)
    model = ApplicationTask

    def get_queryset(self):
        qs = super(ApplicationTaskViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

class ApplicationNotificationViewSet(viewsets.ModelViewSet):
    queryset = ApplicationNotification.objects.all()
    serializer_class = ApplicationNotificationSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    model = ApplicationNotification

    @action(methods=['get'], detail=False, permission_classes=[AllowAny], url_path='login', url_name='login-notifications')
    def get_login_notifications(self, request):
        serializer = ApplicationNotificationSerializer(self.get_queryset().filter(notification_type='login', date_start__lte=datetime.datetime.now(), date_end__gte=datetime.datetime.now()), many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated], url_path='dashboard', url_name='dashboard-notifications')
    def get_dashboard_notifications(self, request):
        serializer = ApplicationNotificationSerializer(self.get_queryset().filter(notification_type='dashboard', date_start__lte=datetime.datetime.now(), date_end__gte=datetime.datetime.now()), many=True, context={'request': request})
        return Response(serializer.data)

class TwoFactorConfigurationViewSet(viewsets.ModelViewSet):
    queryset = TwoFactorConfiguration.objects.all()
    serializer_class = TwoFactorConfigurationSerialiser
    permission_classes = (IsAdminUser,)
    model = TwoFactorConfiguration

    @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated], url_path='enable', url_name='two-factor-enable')
    def put_enable(self, request):
        # Enable 2FA for currently logged in user
        user = get_object_or_404(User, pk=request.user.id)
        TwoFactorConfiguration.objects.create(user=user, totp_key=request.data['totp_key'])
        TwoFactorBackupCode().generate_codes(user=request.user)
        return Response({}, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated], url_path='qr', url_name='two-factor-qr-code')
    def get_qr_code(self, request):
        totp_key = pyotp.random_base32()
        return Response({
            'totp_key': totp_key,
            'url': pyotp.totp.TOTP(totp_key).provisioning_uri(request.user.email, issuer_name="{0} ({1})".format(settings.BRAND_NAME, settings.APP_HOSTNAME if settings.APP_HOSTNAME else 'unknown'))
        }, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False, permission_classes=[IsAuthenticated], url_path='disable', url_name='two-factor-disable')
    def delete_disable(self, request):
        # Disable 2FA for currently logged in user
        user = get_object_or_404(User, pk=request.user.id)
        TwoFactorConfiguration.objects.get(user=user).delete()
        TwoFactorBackupCode.objects.filter(user=user).delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

class TwoFactorBackupCodeViewSet(viewsets.ModelViewSet):
    queryset = TwoFactorBackupCode.objects.all()
    serializer_class = TwoFactorBackupCodeSerializer
    permission_classes = (IsAuthenticated,)
    model = TwoFactorBackupCode

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated], url_path='generate', url_name='two-factor-backup-code-generate')
    def post_generate_backup_codes(self, request):
        codes = TwoFactorBackupCode().generate_codes(user=request.user)
        return Response({ 'codes': codes }, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated], url_path='my', url_name='two-factor-backup-code-my-own')
    def get_my_backup_codes(self, request):
        qs = self.get_queryset()
        if request.user.is_staff:
            qs = qs.filter(user=request.user)
        serializer = TwoFactorBackupCodeSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)