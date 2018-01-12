from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import MessageActionSerializer
from .models import Message
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class MessageActionAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        data = MessageActionSerializer(data=request.data)
        if not data.is_valid():
            return Response(data.data, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.filter(id=data.data.get('message_id')).first()
        if message == None:
            return Response(data.data, status=status.HTTP_404_NOT_FOUND)
        if data.data.get('action') == "spam":
            return self._spam(message)
        if data.data.get('action') == "ham":
            return self._ham(message)
        if data.data.get('action') == "release":
            return self._release(message)

        return Response(data.data, status=status.HTTP_204_NO_CONTENT)

    def _spam(self, message):
        # Here we need to call salearn and pass the parameters
        # needed to learn the message as a spam message
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def _ham(self, message):
        # Here we need to call salear and the parameters
        # needed to learn the message as not harmful
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def _release(self, message):
        # Here we need to instruct the local MTA
        # to resend the message for the intended
        # recipient or an alternate recipient
        return Response({}, status=status.HTTP_204_NO_CONTENT)