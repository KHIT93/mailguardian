from .models import Message, Headers, SpamReport, RblReport, McpReport, MailscannerReport
from .serializers import MessageSerializer, HeaderSerializer, SpamReportSerializer, RblReportSerializer, McpReportSerializer, MailscannerReportSerializer, MessageContentsSerializer, PostqueueStoreMailSerializer, PostqueueStoreSerializer
from mailware.pagination import PageNumberPaginationWithPageCount
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from email.message import EmailMessage
from pymailq.store import PostqueueStore
from django.conf import settings

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    model = Message
    pagination_class = PageNumberPaginationWithPageCount
    permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='contents', url_name='message-file-contents')
    def get_message_contents(self, request, pk=None):
        message = get_object_or_404(Message.objects.all(), pk=pk)
        data = { 'message_id':message.id, 'mailq_id': message.mailq_id, 'message_contents': None }
        if message.queue_file_exists():
            f = open(message.file_path())
            m = EmailMessage()
            m.set_content(f.read())
            data['message_contents'] = m
            f.close()
        
        serializer = MessageContentsSerializer(data)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False, permission_classes=[IsAdminUser], url_path='queue', url_name='message-queue')
    def get_queue(self, request):
        store = PostqueueStore()
        store.load()
        serializer = PostqueueStoreSerializer({ 'mails':store.mails, 'loaded_at':store.loaded_at })
        return Response(serializer.data)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated], url_path='action', url_name='message-action')
    def post_action(self, request, pk=None):
        message = get_object_or_404(Message.objects.all(), pk=pk)
        data = request.data['data']
        action = request.data['action']
        if not isinstance(data, list):
            data = [data]
        # At this point we should pass the message(s) to Celery for processing
        # and return a response to the client
        for message in data:
            if action == "spam":
                return self._spam(message)
            if action == "ham":
                return self._ham(message)
            if action == "release":
                return self._release(message)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def _spam(self, message):
        # Here we need to call salearn and pass the parameters
        # needed to learn the message as a spam message
        command = "sudo {0} -p {1} -r {2}".format(settings.SA_BIN, settings.MAILSCANNER_CONFIG_DIR + '/spamassassin.conf', message.file_path())
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def _ham(self, message):
        # Here we need to call salear and the parameters
        # needed to learn the message as not harmful
        command = "sudo {0} -p {1} -k {2}".format(settings.SA_BIN, settings.MAILSCANNER_CONFIG_DIR + '/spamassassin.conf', message.file_path())
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def _release(self, message):
        # Here we need to instruct the local MTA
        # to resend the message for the intended
        # recipient or an alternate recipient
        # sendmail -i -f REPLY_TO_ADDRESS TO_ADDRESS FILEPATH_TO_MESSAGE 2>&1
        command = "sudo {0} -i -f {1} {2} {3} 2>&1".format(settings.SENDMAIL_BIN, "", message.to_address, message.file_path())
        message.released = True
        message.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

class HeaderViewSet(viewsets.ModelViewSet):
    queryset = Headers.objects.all()
    serializer_class = HeaderSerializer
    model = Headers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.query_params.__contains__('message'):
            return self.queryset.filter(message_id=self.request.query_params.get('message'))
        else:
            return self.queryset

class SpamReportViewSet(viewsets.ModelViewSet):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    model = SpamReport
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.query_params.__contains__('message'):
            return self.queryset.filter(message_id=self.request.query_params.get('message'))
        else:
            return self.queryset

class RblReportViewSet(viewsets.ModelViewSet):
    queryset = RblReport.objects.all()
    serializer_class = RblReportSerializer
    model = RblReport
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.query_params.__contains__('message'):
            return self.queryset.filter(message_id=self.request.query_params.get('message'))
        else:
            return self.queryset

class MailscannerReportViewSet(viewsets.ModelViewSet):
    queryset = MailscannerReport.objects.all()
    serializer_class = MailscannerReportSerializer
    model = MailscannerReport
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.query_params.__contains__('message'):
            return self.queryset.filter(message_id=self.request.query_params.get('message'))
        else:
            return self.queryset

class McpReportViewSet(viewsets.ModelViewSet):
    queryset = McpReport.objects.all()
    serializer_class = McpReportSerializer
    model = McpReport
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.query_params.__contains__('message'):
            return self.queryset.filter(message_id=self.request.query_params.get('message'))
        else:
            return self.queryset