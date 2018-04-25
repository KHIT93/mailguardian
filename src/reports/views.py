from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django.db.models import Count, Sum
from mail.models import Message
from mail.serializers import MessageSerializer
from .filters import MessageQuerySetFilter
from .serializers import MessagesByDateSerializer, MessageRelaysSerializer, MessagesPerHourSerializer, TopSendersByQuantitySerializer, TopSendersByVolumeSerializer, TopRecipientsByQuantitySerializer, TopRecipientsByVolumeSerializer, TopSenderDomainsByQuantitySerializer, TopSenderDomainsByVolumeSerializer, TopRecipientDomainsByQuantitySerializer, TopRecipientDomainsByVolumeSerializer
from mailware.pagination import PageNumberPaginationWithPageCount
import json, datetime

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

class MessagesPerHourApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.values('timestamp').filter(timestamp__range=[datetime.datetime.now() - datetime.timedelta(days=1), datetime.datetime.now()]), filters)
        serializer = MessagesPerHourSerializer(qs.annotate(Count('id')).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)

class TopSendersByQuantityApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.values('from_address'), filters)
        serializer = TopSendersByQuantitySerializer(qs.annotate(Count('id')).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)

class TopSendersByVolumeApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.values('from_address'), filters)
        serializer = TopSendersByVolumeSerializer(qs.annotate(Sum('size')).order_by('-size__sum')[:10], many=True)
        return Response(serializer.data, 200)

class TopRecipientsByQuantityApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.values('to_address'), filters)
        serializer = TopRecipientsByQuantitySerializer(qs.annotate(Count('id')).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)

class TopRecipientsByVolumeApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.values('to_address'), filters)
        serializer = TopRecipientsByVolumeSerializer(qs.annotate(Sum('size')).order_by('-size__sum')[:10], many=True)
        return Response(serializer.data, 200)

class TopSenderDomainsByQuantityApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.values('from_domain'), filters)
        serializer = TopSenderDomainsByQuantitySerializer(qs.annotate(Count('id')).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)

class TopSenderDomainsByVolumeApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.values('from_domain'), filters)
        serializer = TopSenderDomainsByVolumeSerializer(qs.annotate(Sum('size')).order_by('-size__sum')[:10], many=True)
        return Response(serializer.data, 200)

class TopRecipientDomainsByQuantityApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.values('to_domain'), filters)
        serializer = TopRecipientDomainsByQuantitySerializer(qs.annotate(Count('id')).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)

class TopRecipientDomainsByVolumeApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.values('to_domain'), filters)
        serializer = TopRecipientDomainsByVolumeSerializer(qs.annotate(Sum('size')).order_by('-size__sum')[:10], many=True)
        return Response(serializer.data, 200)