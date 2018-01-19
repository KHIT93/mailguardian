from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from mail.models import Message
from mail.serializers import MessageSerializer
from .filters import MessageQuerySetFilter
from mailware.pagination import PageNumberPaginationWithPageCount

class SummaryApiView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPaginationWithPageCount
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, Message.objects.all(), filters)
        response_data = {
            'latest': qs.latest().timestamp,
            'earliest': qs.earliest().timestamp,
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