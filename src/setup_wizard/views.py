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
from django.core.management import call_command
from io import StringIO
import django

# Create your views here.
class LicenseAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        license = ""
        with open(os.path.join(os.path.dirname(settings.BASE_DIR), "LICENSE")) as f:
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
            'django_version': django.VERSION,
            'mailguardian_api_version': '1.0.0',
            'mailguardian_version': '1.0.0',
            'mailguardian_multi_node': multi_node,
            'mailguardian_host': settings.APP_HOSTNAME
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
            user = User.objects.create_superuser(serializer.admin_email, serializer.admin_password)
            response['createsuperuser'] = user
            # Next create initial core.models.Setting entries based on the remaining data provided by the user
            Setting.objects.update_or_create(key='quarantine.report.daily', defaults={'key' : 'quarantine.report.daily', 'value' : serializer.quarantine_report_daily})
            Setting.objects.update_or_create(key='quarantine.report.from', defaults={'key' : 'quarantine.report.from', 'value' : serializer.quarantine_report_from})
            Setting.objects.update_or_create(key='quarantine.report.non_spam.hide', defaults={'key' : 'quarantine.report.non_spam.hide', 'value' : serializer.quarantine_report_non_spam_hide})
            Setting.objects.update_or_create(key='quarantine.report.subject', defaults={'key' : 'quarantine.report.subject', 'value' : serializer.quarantine_report_subject})
            response['createsettings'] = 'Initial settings have been configured'
            # Last update guardianware-env.json with the branding information of the application
            with open(os.path.join(os.path.dirname(BASE_DIR), "mailguardian-env.json"), 'w') as f:
                data = f.read()
                data.replace('"name": "MailGuardian"', '"name": "{0}"'.format(serializer.branding_name))
                data.replace('"tagline": "Securing your email"', '"tagline": "{0}"'.format(serializer.branding_tagline))
                data.replace('"logo": ""', '"logo": "{0}"'.format(serializer.branding_logo))
                f.write(data)
                response['update_env'] = 'Environment file succesfully updated. Please run "sudo systemctl restat mailguardian.service"'
            return Response(response, status=status.HTTP_200_OK)

