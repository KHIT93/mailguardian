from .models import Message, Headers, SpamReport, RblReport, McpReport, MailscannerReport
from .serializers import MessageSerializer, HeaderSerializer, SpamReportSerializer, RblReportSerializer, McpReportSerializer, MailscannerReportSerializer
from mailware.pagination import PageNumberPaginationWithPageCount
from rest_framework import viewsets

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    model = Message
    pagination_class = PageNumberPaginationWithPageCount

class HeaderViewSet(viewsets.ModelViewSet):
    queryset = Headers.objects.all()
    serializer_class = HeaderSerializer
    model = Headers

    def get_queryset(self):
        if self.request.query_params.__contains__('message'):
            return Headers.objects.filter(message_id=self.request.query_params.get('message'))
        else:
            return Headers.objects.all()

class SpamReportViewSet(viewsets.ModelViewSet):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    model = SpamReport

    def get_queryset(self):
        if self.request.query_params.__contains__('message'):
            return SpamReport.objects.filter(message_id=self.request.query_params.get('message'))
        else:
            return SpamReport.objects.all()

class RblReportViewSet(viewsets.ModelViewSet):
    queryset = RblReport.objects.all()
    serializer_class = RblReportSerializer
    model = RblReport

    def get_queryset(self):
        if self.request.query_params.__contains__('message'):
            return RblReport.objects.filter(message_id=self.request.query_params.get('message'))
        else:
            return RblReport.objects.all()

class MailscannerReportViewSet(viewsets.ModelViewSet):
    queryset = MailscannerReport.objects.all()
    serializer_class = MailscannerReportSerializer
    model = MailscannerReport

    def get_queryset(self):
        if self.request.query_params.__contains__('message'):
            return MailscannerReport.objects.filter(message_id=self.request.query_params.get('message'))
        else:
            return MailscannerReport.objects.all()

class McpReportViewSet(viewsets.ModelViewSet):
    queryset = McpReport.objects.all()
    serializer_class = McpReportSerializer
    model = McpReport

    def get_queryset(self):
        if self.request.query_params.__contains__('message'):
            return McpReport.objects.filter(message_id=self.request.query_params.get('message'))
        else:
            return McpReport.objects.all()