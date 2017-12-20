from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

class CurrentUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def get_permissions(self):
        return (IsAuthenticated()),