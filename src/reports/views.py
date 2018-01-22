from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django.db.models import Count
from mail.models import Message
from mail.serializers import MessageSerializer
from .filters import MessageQuerySetFilter
from .serializers import MessagesByDateSerializer, MessageRelaysSerializer
from mailware.pagination import PageNumberPaginationWithPageCount
import json

class SummaryApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.all(), filters)
        response_data = {
            'latest': qs.latest().date,
            'earliest': qs.earliest().date,
            'count': qs.count()
        }
        return Response(response_data, 200)

class MessageListApiView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPaginationWithPageCount
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.all(), filters)
        self.queryset = qs
        return self.list(request)

class MessagesByDateApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.values('date'), filters)
        serializer = MessagesByDateSerializer(qs.annotate(Count('id')).order_by('date'), many=True)
        return Response(serializer.data, 200)

class TopMailRelaysApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.values('client_ip'), filters)
        serializer = MessageRelaysSerializer(qs.annotate(Count('id')).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)