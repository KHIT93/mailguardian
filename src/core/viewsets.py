from .models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import MailScannerConfiguration, Setting, AuditLog
from .serializers import UserSerializer, MailScannerConfigurationSerializer, SettingsSerializer, AuditLogSerializer
from django.db.models import Q
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    model = User

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
        if not 'key' in request.POST:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        entity = get_object_or_404(Setting, key=request.POST['key'])
        serializer = SettingsSerializer(entity, context={'request': request})
        return Response(serializer.data)

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = (IsAdminUser,)
    model = AuditLog