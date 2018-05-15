from .models import User
from rest_framework import serializers
from .models import MailScannerConfiguration, Setting, AuditLog

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'email', 'is_staff', 'is_domain_admin', 'is_active', 'first_name', 'last_name', 'full_name', 'date_joined')

    full_name = serializers.SerializerMethodField()
    # mailuser = MailUserSerializer(many=False, read_only=True)

    def get_full_name(self, obj):
        obj.get_full_name()

class MailScannerConfigurationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailScannerConfiguration
        fields = ('id', 'url', 'key', 'value', 'filepath')

class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Setting
        fields = ('id', 'url', 'key', 'value')

class AuditLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AuditLog
        fields = ('id', 'url', 'user', 'ip_address', 'timestamp', 'module', 'action', 'message')