from rest_framework import serializers
from .models import (
    Setting,
    User,
    MailScannerHost,
    ApplicationNotification,
)
from dj_rest_auth.serializers import PasswordResetSerializer
from trench.serializers import UserMFAMethodSerializer
from django.conf import settings
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
            'has_two_factor',
            'mfa_method_count',
            'mfa_methods'
        )

    full_name = serializers.SerializerMethodField()
    has_two_factor = serializers.SerializerMethodField()
    mfa_method_count = serializers.SerializerMethodField()
    mfa_methods = UserMFAMethodSerializer(many=True)
    # mailuser = MailUserSerializer(many=False, read_only=True)

    def get_full_name(self, obj):
        obj.get_full_name()
        
    def get_has_two_factor(self, obj):
        return obj.has_mfa
            
    def get_mfa_method_count(self, obj):
        return obj.mfa_method_count

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
            'has_two_factor',
            'mfa_method_count',
            'mfa_methods',
        )
        read_only_fields = (
            'is_staff',
            'is_domain_admin',
            'is_active',
            'date_joined',
        )

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

class ApplicationNotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ApplicationNotification
        fields = ('id', 'url', 'title', 'body', 'date_start', 'date_end', 'notification_type')

