from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from domains.models import Domain
from .models import (
    Setting,
    User,
    MailScannerHost,
    ApplicationNotification,
)
from .serializers import (
    UserSerializer,
    SettingsSerializer,
    ChangePasswordSerializer,
    MailScannerHostSerializer,
    ApplicationNotificationSerializer,
)
from django.db.models import Q
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from domains.serializers import DomainSerializer
from .permissions import IsDomainAdminOrStaff, IsAdminUserOrReadOnly
from rest_framework.permissions import AllowAny
from django.conf import settings
import datetime, pyotp
from django.utils.translation import gettext_lazy as _
from compliance.models import DataLogEntry

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsDomainAdminOrStaff,)
    model = User

    def get_queryset(self):
        qs = super(UserViewSet, self).get_queryset()
        if self.request.query_params.__contains__('search'):
            search_key = self.request.query_params.get('search')
            qs = qs.filter(
                    Q(email__icontains=search_key) | Q(first_name__icontains=search_key) | Q(last_name__icontains=search_key)
                )
        if self.request.user.is_staff:
            return qs
        domains = [domain.name for domain in self.request.user.domains.all()]
        qs = qs.filter(domains__name__in=domains).distinct()
        return qs

    @action(methods=['get'], detail=True, permission_classes=[IsDomainAdminOrStaff], url_path='domains', url_name='get-user-domains')
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

class MailScannerHostViewSet(viewsets.ModelViewSet):
    queryset = MailScannerHost.objects.all()
    serializer_class = MailScannerHostSerializer
    permission_classes = (IsAdminUser,)
    model = MailScannerHost

    def get_queryset(self):
        qs = self.queryset
        if self.request.query_params.__contains__('search'):
            search_key = self.request.query_params.get('search')
            qs = qs.filter(
                    Q(hostname__icontains=search_key) | Q(ip_address__icontains=search_key)
                )
        if self.request.query_params.__contains__('filename'):
            qs = qs.filter(filepath=self.request.query_params.get('filename'))
        return qs

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
