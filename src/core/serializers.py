from .models import User
from rest_framework import serializers
from .models import MailScannerConfiguration, Setting, AuditLog
from rest_auth.serializers import PasswordResetSerializer
from django.conf import settings

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'email', 'is_staff', 'is_domain_admin', 'is_active', 'first_name', 'last_name', 'full_name', 'date_joined', 'domains')

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

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=False)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

class MailwarePasswordResetSerializer(PasswordResetSerializer):
    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'email_template_name': 'mailware/registration/password_reset_email.html'
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)