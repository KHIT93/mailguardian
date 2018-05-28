from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from .permissions import ApplicationNotInstalled

# Create your views here.
class LicenseAPIView(APIView):
    permission_classes = (ApplicationNotInstalled,)
    def get(self, request):
        license = ""
        with open(os.path.join(os.path.dirname(settings.BASE_DIR), "LICENSE")) as f:
            license = f.read()
        return Response(license, 200)

class InstalledAPIView(APIView):
    permission_classes = (ApplicationNotInstalled,)
    def post(self, request):
        return Response({}, 204)

class InitializeDatabaseAPIView(APIView):
    permission_classes = (ApplicationNotInstalled,)
    def post(self, request):
        pass
