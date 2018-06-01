from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import connection
import os
from .permissions import ApplicationNotInstalled

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
        return Response({
            'django_version': '2.0.5',
            'mailware_api_version': '1.0.0',
            'mailware_version': '1.0.0'
        }, 200)

class InitializeDatabaseAPIView(APIView):
    permission_classes = (ApplicationNotInstalled,)
    def post(self, request):
        pass
