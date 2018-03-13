from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import MailScannerConfiguration
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class CurrentUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def get_permissions(self):
        return (IsAuthenticated()),

class MailScannerConfigurationFilePathsView(APIView):
    def get(self, request):
        files = MailScannerConfiguration.objects.values('filepath').distinct()
        return Response(files)
    
    def get_permissions(self):
        return (IsAdminUser()),
