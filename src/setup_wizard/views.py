from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db import connection
import os
from .permissions import ApplicationNotInstalled
from .serializers import InitialDataSerializer
from core.models import User, Setting, MailScannerHost
from core.serializers import UserSerializer
from django.core.management import call_command
from io import StringIO
import django, json
from django.utils.translation import gettext_lazy as _
from pathlib import Path

# Create your views here.
class LicenseAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        license = ""
        with open(Path(settings.BASE_DIR.parent, "LICENSE")) as f:
            license = f.read()
        return Response(license, 200)

class InstalledAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        cursor = connection.cursor()
        table_names = connection.introspection.get_table_list(cursor)
        if len(table_names) == 0:
            return Response({}, 204)
        host_count = MailScannerHost.objects.count()
        multi_node = True if host_count > 0 else False

        return Response({
            'framework_version': '.'.join([str(x) for x in django.VERSION]),
            'api_version': settings.APP_VERSION,
            'app_version': settings.APP_VERSION,
            'multi_node': multi_node,
            'host': settings.APP_HOSTNAME,
            'app_name': settings.BRAND_NAME,
            'app_logo': settings.BRAND_LOGO,
            'app_feedback': settings.BRAND_FEEDBACK,
            'app_support': settings.BRAND_SUPPORT
        }, 200)

class InitializeDatabaseAPIView(APIView):
    permission_classes = (ApplicationNotInstalled,)
    def post(self, request):
        serializer = InitialDataSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = {
                'migrate': '',
                'createsuperuser': '',
                'createsettings': '',
                'update_env': ''
            }
            # First migrate the database and store the command output
            output = StringIO()
            call_command('migrate', stdout=output)
            response['migrate'] = output.getvalue()
            # Next create a superuser based on the admin_email and admin_password values
            user = User.objects.create_superuser(serializer.data['admin_email'], serializer.data['admin_password'])
            response['createsuperuser'] = UserSerializer(user, context={'request': request}).data
            # Next create initial core.models.Setting entries based on the remaining data provided by the user
            Setting.objects.update_or_create(key='quarantine.report.days', defaults={'key' : 'quarantine.report.days', 'value' : '7'})
            Setting.objects.update_or_create(key='quarantine.report.unknown.hide', defaults={'key' : 'quarantine.report.unknown.hide', 'value' : '1'})
            Setting.objects.update_or_create(key='sa.last_updated', defaults={'key' : 'sa.last_updated', 'value' : ''})
            Setting.objects.update_or_create(key='quarantine.release.body', defaults={'key' : 'quarantine.release.body', 'value' : 'Please find the original message that was quarantined attached to this mail.Regards,Postmaster'})
            Setting.objects.update_or_create(key='quarantine.filters.combine', defaults={'key' : 'quarantine.filters.combine', 'value' : '1'})
            Setting.objects.update_or_create(key='mailscanner.configuration.edit', defaults={'key' : 'mailscanner.configuration.edit', 'value' : '0'})
            Setting.objects.update_or_create(key='mailscanner.rules.edit', defaults={'key' : 'mailscanner.rules.edit', 'value' : '0'})
            Setting.objects.update_or_create(key='mail.spamassassin.score', defaults={'key' : 'mail.spamassassin.score', 'value' : '5'})
            Setting.objects.update_or_create(key='mail.spamassassin.highscore', defaults={'key' : 'mail.spamassassin.highscore', 'value' : '15'})

            Setting.objects.update_or_create(key='quarantine.report.daily', defaults={'key' : 'quarantine.report.daily', 'value' : serializer.data['quarantine_report_daily']})
            Setting.objects.update_or_create(key='quarantine.report.weekly', defaults={'key' : 'quarantine.report.weekly', 'value' : True})
            Setting.objects.update_or_create(key='quarantine.report.monthly', defaults={'key' : 'quarantine.report.monthly', 'value' : False})
            Setting.objects.update_or_create(key='quarantine.report.from', defaults={'key' : 'quarantine.report.from', 'value' : serializer.data['quarantine_report_from']})
            Setting.objects.update_or_create(key='quarantine.report.non_spam.hide', defaults={'key' : 'quarantine.report.non_spam.hide', 'value' : serializer.data['quarantine_report_non_spam_hide']})
            Setting.objects.update_or_create(key='quarantine.report.subject', defaults={'key' : 'quarantine.report.subject', 'value' : serializer.data['quarantine_report_subject']})
            response['createsettings'] = _('Initial settings have been configured')
            # Last update guardianware-env.json with the branding information of the application
            data = []
            with open(Path(settings.BASE_DIR.parent, 'src', 'mailguardian', 'settings', 'local.py'), 'r') as f:
                data = f.readlines()
            for index, line in enumerate(data):
                if line[:10] == 'BRAND_NAME':
                    data[index] = 'BRAND_NAME = "{}"'.format(serializer.data['branding_name'])
                if line[:13] == 'BRAND_TAGLINE':
                    data[index] = 'BRAND_TAGLINE = "{}"'.format(serializer.data['branding_tagline'])
                if line[:10] == 'BRAND_LOGO':
                    data[index] = 'BRAND_LOGO = "{}"'.format(serializer.data['branding_logo'])
            
            with open(Path(settings.BASE_DIR.parent, 'src', 'mailguardian', 'settings', 'local.py'), 'w') as f:
                f.write("\n".join(data))
            response['update_env'] = _('Settings file succesfully updated. Please run "sudo systemctl restart mailguardian.service"')
            return Response(response, status=status.HTTP_200_OK)

