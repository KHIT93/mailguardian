from rest_framework import serializers
from .models import MailScannerConfiguration, Setting, User, MailScannerHost
from rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
from auditlog.models import LogEntry as AuditLog
from django_celery_results.models import TaskResult
import json

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'email', 'is_staff', 'is_domain_admin', 'is_active', 'first_name', 'last_name', 'full_name', 'date_joined', 'domains', 'daily_quarantine_report', 'weekly_quarantine_report', 'monthly_quarantine_report', 'custom_spam_score', 'custom_spam_highscore', 'skip_scan')

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
        fields = ('id', 'url', 'module', 'object_pk', 'object_id', 'object_repr', 'action', 'action_name', 'changes', 'actor_id', 'actor_email', 'remote_addr', 'timestamp', 'additional_data')
    module = serializers.SerializerMethodField()
    actor_email = serializers.SerializerMethodField()
    changes = serializers.SerializerMethodField()
    action_name = serializers.SerializerMethodField()

    def get_module(self, obj):
        return obj.content_type.app_label + ':' + obj.content_type.model

    def get_actor_email(self, obj):
        return obj.actor.email if obj.actor else 'System'
    
    def get_changes(self, obj):
        return json.loads(obj.changes)

    def get_action_name(self, obj):
        if obj.action == 0:
            return 'Create'
        elif obj.action == 1:
            if 'last_login' in self.get_changes(obj) and obj.content_type.model == 'user':
                return 'Login'
            elif 'password' in self.get_changes(obj) and obj.content_type.model == 'user':
                return 'Change password'
            elif 'released' in self.get_changes(obj) and self.get_changes(obj).released[1] == True and obj.content_type == 'message':
                return 'Message released'
            return 'Update'
        elif obj.action == 2:
            return 'Delete'

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
        fields = ('id', 'url', 'hostname', 'ip_address', 'use_tls', 'priority')