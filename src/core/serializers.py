from rest_framework import serializers
from .models import MailScannerConfiguration, Setting, User, MailScannerHost
from rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
from auditlog.models import LogEntry as AuditLog
from django_celery_results.models import TaskResult

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'email', 'is_staff', 'is_domain_admin', 'is_active', 'first_name', 'last_name', 'full_name', 'date_joined', 'domains', 'custom_spam_score', 'custom_spam_highscore', 'skip_scan')

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
        fields = ('id', 'url', 'module', 'object_pk', 'object_id', 'object_repr', 'action', 'changes', 'actor_id', 'remote_addr', 'timestamp', 'additional_data')
    module = serializers.SerializerMethodField()

    def get_module(self, obj):
        return obj.content_type.app_label + ':' + obj.content_type.model

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

class MailGuardianPasswordResetSerializer(PasswordResetSerializer):
    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'email_template_name': 'mailguardian/registration/password_reset_email.html'
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)

class TaskResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskResult
        fields = ('task_id', 'task_name', 'task_args', 'task_kwargs', 'status', 'content_type', 'content_encoding', 'result', 'date_done', 'traceback', 'hidden', 'meta')

class MailScannerHostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailScannerHost
        fields = ('id', 'url', 'hostname', 'ip_address', 'use_tls')