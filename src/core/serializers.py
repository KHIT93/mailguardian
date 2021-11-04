from rest_framework import serializers
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
from rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
import json
from rest_auth.serializers import LoginSerializer as BaseRestAuthLoginSerializer
from django.utils.translation import gettext_lazy as _

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_staff',
            'is_domain_admin',
            'is_active',
            'first_name',
            'last_name',
            'full_name',
            'date_joined',
            'domains',
            'daily_quarantine_report',
            'weekly_quarantine_report',
            'monthly_quarantine_report',
            'custom_spam_score',
            'custom_spam_highscore',
            'skip_scan',
            'has_two_factor'
        )

    full_name = serializers.SerializerMethodField()
    has_two_factor = serializers.SerializerMethodField()
    # mailuser = MailUserSerializer(many=False, read_only=True)

    def get_full_name(self, obj):
        obj.get_full_name()
        
    def get_has_two_factor(self, obj):
        return obj.get_has_two_factor()
            

class AccountUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_staff',
            'is_domain_admin',
            'is_active',
            'first_name',
            'last_name',
            'full_name',
            'date_joined',
            'domains',
            'daily_quarantine_report',
            'weekly_quarantine_report',
            'monthly_quarantine_report',
            'custom_spam_score',
            'custom_spam_highscore',
            'skip_scan',
            'has_two_factor'
        )
        read_only_fields = (
            'is_staff',
            'is_domain_admin',
            'is_active',
            'date_joined',
        )


class MailScannerConfigurationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailScannerConfiguration
        fields = ('id', 'url', 'key', 'value', 'filepath')

class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Setting
        fields = ('id', 'url', 'key', 'value')

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

class MailGuardianPasswordResetSerializer(PasswordResetSerializer):
    def save(self):
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
        try:
            from_email = Setting.objects.get(key='quarantine.report.from').value
        except:
            pass
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': from_email,
            'request': request,
            'email_template_name': 'mailguardian/registration/password_reset_email.html'
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)

class MailScannerHostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailScannerHost
        fields = ('id', 'url', 'hostname', 'ip_address', 'use_tls', 'priority', 'passive')

class ApplicationTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ApplicationTask
        fields = ('id', 'url', 'user_email', 'hostname', 'created', 'updated', 'completed', 'status_code', 'status_message', 'content_type_id', 'object_pk', 'method', 'params')
    hostname = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()

    def get_hostname(self, obj):
        return obj.host.name

    def get_user_email(self, obj):
        return obj.user.email

class ApplicationNotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ApplicationNotification
        fields = ('id', 'url', 'title', 'body', 'date_start', 'date_end', 'notification_type')

class LoginSerializer(BaseRestAuthLoginSerializer):
    two_factor_token = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    backup_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)

class TwoFactorConfigurationSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TwoFactorConfiguration
        fields = ('id', 'url', 'user', 'totp_key')

class TwoFactorBackupCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TwoFactorBackupCode
        fields = ('id', 'url', 'user', 'code')
