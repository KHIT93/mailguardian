from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import MailScannerConfiguration, Setting, User, MailScannerHost, ApplicationTask
from .serializers import UserSerializer, MailScannerConfigurationSerializer, SettingsSerializer, ChangePasswordSerializer, AuditLogSerializer, MailScannerHostSerializer, ApplicationTaskSerializer
from django.db.models import Q
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from domains.serializers import DomainSerializer
from .permissions import IsDomainAdminOrStaff
from auditlog.models import LogEntry as AuditLog

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
                return Response({"new_password1": ["The passwords do not match."], "new_password2": ["The passwords do not match."]}, status=status.HTTP_400_BAD_REQUEST)
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