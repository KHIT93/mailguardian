from .models import Message, Headers, SpamReport, RblReport, McpReport
from .serializers import MessageSerializer, HeaderSerializer, SpamReportSerializer, RblReportSerializer, McpReportSerializer
from rest_framework import viewsets

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    model = Message

class HeaderViewSet(viewsets.ModelViewSet):
    queryset = Headers.objects.all()
    serializer_class = HeaderSerializer
    model = Headers

class SpamReportViewSet(viewsets.ModelViewSet):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    model = SpamReport

class RblReportViewSet(viewsets.ModelViewSet):
    queryset = RblReport.objects.all()
    serializer_class = RblReportSerializer
    model = RblReport

class McpReportViewSet(viewsets.ModelViewSet):
    queryset = McpReport.objects.all()
    serializer_class = McpReportSerializer
    model = McpReport