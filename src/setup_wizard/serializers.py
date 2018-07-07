from rest_framework import serializers

class InitialDataSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField()
    branding_name = serializers.CharField()
    branding_tagline = serializers.CharField(allow_blank=True)
    branding_logo = serializers.CharField(allow_blank=True)
    quarantine_report_from = serializers.EmailField()
    quarantine_report_subject = serializers.CharField()
    quarantine_report_daily = serializers.BooleanField()
    quarantine_report_non_spam_hide = serializers.BooleanField()
