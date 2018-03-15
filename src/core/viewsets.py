from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import MailScannerConfiguration, Setting
from .serializers import UserSerializer, MailScannerConfigurationSerializer, SettingsSerializer
from django.db.models import Q

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