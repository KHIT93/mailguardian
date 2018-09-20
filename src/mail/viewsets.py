from .models import Message, Headers, SpamReport, RblReport, McpReport, MailscannerReport, TransportLog, SmtpRelay
from .serializers import MessageSerializer, HeaderSerializer, SpamReportSerializer, RblReportSerializer, McpReportSerializer, MailscannerReportSerializer, MessageContentsSerializer, PostqueueStoreMailSerializer, PostqueueStoreSerializer, TransportLogSerializer, SmtpRelaySerializer
from mailguardian.pagination import PageNumberPaginationWithPageCount
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from email import policy
from email.parser import BytesParser
from pymailq.store import PostqueueStore
from django.conf import settings
from core.models import Setting, MailScannerHost
import datetime
from django.db.models import Q
import subprocess
import requests, json, types
from rest_framework.authtoken.models import Token

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    model = Message
    pagination_class = PageNumberPaginationWithPageCount
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(MessageViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return qs
        domains = [domain.name for domain in self.request.user.domains.all()]
        qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        return qs

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='contents', url_name='message-file-contents')
    def get_message_contents(self, request, pk=None):
        message = get_object_or_404(self.get_queryset(), pk=pk)
        data = { 'message_id':message.id, 'mailq_id': message.mailq_id, 'message_contents': None }
        if message.queue_file_exists():
            data = None
            if message.mailscanner_hostname != settings.APP_HOSTNAME:
                token = Token.objects.get(user=request.user)
                host = MailScannerHost.objects.get(hostname=message.mailscanner_hostname)
                protocol = 'https' if host.use_tls else 'http'
                url = '{0}://{1}/api/messages/{2}/contents/'.format(protocol, host.hostname, pk)
                headers = {
                    'Content-Type' : 'application/json',
                    'Authorization' : 'Token {0}'.format(token.key)
                }
                result = requests.get(url, headers=headers)
                data = json.loads(result.content.decode('utf-8'))
            else:
                m = None
                data = {
                    'message': {
                    'message_id': message.id,
                    'mailq_id': message.mailq_id
                    }
                }
                with open(message.file_path()) as fp:
                    m = BytesParser(policy=policy.default).parse(fp)
                simplest = m.get_body(preferencelist=('plain', 'html'))
                richest = m.get_body()
                data['message']['simple_type'] = "{0}/{1}".format(simplest['content-type'].maintype, simplest['content-type'].subtype)
                data['message']['rich_type'] = "{0}/{1}".format(richest['content-type'].maintype, richest['content-type'].subtype)
                if simplest['content-type'].subtype == 'html':
                    data['message']['simple_version'] = ''
                else:
                    data['message']['simple_version'] = simplest
                if richest['content-type'].subtype == 'html':
                    data['message']['rich_version'] = richest
                elif richest['content-type'].content_type == 'multipart/related':
                    data['message']['rich_version'] = richest.get_body(preferencelist=('html'))
                    data['message']['attachments'] = []
                    for part in richest.iter_attachments():
                        data['message']['attachments'].append(part.get_filename())
                else:
                    data['message']['rich_version'] = 'Preview unavailable'
        return Response(data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='file-exists', url_name='message-queue-file-exists')
    def get_file_exists(self, request, pk=None):
        message = get_object_or_404(self.get_queryset(), pk=pk)
        file_exists = False
        data = None
        error = None
        url = None
        if message.mailscanner_hostname != settings.APP_HOSTNAME:
            #try:
            token = Token.objects.get(user=request.user)
            host = MailScannerHost.objects.get(hostname=message.mailscanner_hostname)
            protocol = 'https' if host.use_tls else 'http'
            url = '{0}://{1}/api/messages/{2}/file-exists/'.format(protocol, host.hostname, pk)
            headers = {
                'Content-Type' : 'application/json',
                'Authorization' : 'Token {0}'.format(token.key)
            }
            result = requests.get(url, headers=headers)
            data = json.loads(result.content.decode('utf-8'))
            file_exists = data['file_exists']
            #except Exception as e:
            #    error = e
        else:
            file_exists = message.queue_file_exists()
        return Response({
            'message_id': pk,
            'file_exists': file_exists,
            'error': error
        })

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='transport-log', url_name='message-transport-logs')
    def get_message_transport_logs(self, request, pk=None):
        message = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = TransportLogSerializer(message.transportlog_set.all(), many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='headers', url_name='message-headers')
    def get_message_headers(self, request, pk=None):
        message = get_object_or_404(self.get_queryset(), pk=pk)
        if not hasattr(message, 'headers'):
            return Response({}, status.HTTP_204_NO_CONTENT)
        serializer = HeaderSerializer(message.headers, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='rbl-report', url_name='message-rbl-report')
    def get_message_rbl_report(self, request, pk=None):
        message = get_object_or_404(self.get_queryset(), pk=pk)
        if not hasattr(message, 'rblreport'):
            return Response({}, status.HTTP_204_NO_CONTENT)
        serializer = RblReportSerializer(message.rblreport, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='spam-report', url_name='message-spam-report')
    def get_message_spam_report(self, request, pk=None):
        message = get_object_or_404(self.get_queryset(), pk=pk)
        if not hasattr(message, 'spamreport'):
            return Response({}, status.HTTP_204_NO_CONTENT)
        serializer = SpamReportSerializer(message.spamreport, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='mcp-report', url_name='message-mcp-report')
    def get_message_mcp_report(self, request, pk=None):
        message = get_object_or_404(self.get_queryset(), pk=pk)
        if not hasattr(message, 'mcpreport'):
            return Response({}, status.HTTP_204_NO_CONTENT)
        serializer = McpReportSerializer(message.mcpreport, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='mailscanner-report', url_name='message-mailscanner-report')
    def get_message_mailscanner_report(self, request, pk=None):
        message = get_object_or_404(self.get_queryset(), pk=pk)
        if not hasattr(message, 'mailscannerreport'):
            return Response({}, status.HTTP_204_NO_CONTENT)
        serializer = MailscannerReportSerializer(message.mailscannerreport, context={'request': request})
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False, permission_classes=[IsAdminUser], url_path='queue', url_name='message-queue')
    def get_queue(self, request):
        store = PostqueueStore()
        store.load()
        serializer = PostqueueStoreSerializer({ 'mails':store.mails, 'loaded_at':store.loaded_at })
        return Response(serializer.data)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated], url_path='release', url_name='message-action-release')
    def post_action_release(self, request):
        if not 'messages' in request.data:
            return Response({'error': 'No messages to process'}, status=status.HTTP_400_BAD_REQUEST)
        # Here we need to instruct the local MTA
        # to resend the message for the intended
        # recipient or an alternate recipient
        # sendmail -i -f REPLY_TO_ADDRESS TO_ADDRESS < FILEPATH_TO_MESSAGE 2>&1
        
        response = []
        sender = Setting.objects.get(key='mail.release.sender')
        recv_messages = []
        if isinstance(request.data['messages'], list):
            recv_messages = request.data['messages']
        elif isinstance(request.data['message'], types.StringType):
            recv_messages.append(request.data['messages'])
        for message_id in request.data['messages']:
            try:
                message = Message.objects.get(id=message_id)
                if message.released:
                    response.append({'id': message_id, 'error': 'This message has already been released'})
                elif settings.APP_HOSTNAME == message.mailscanner_hostname:
                    command = "{0} -i -f {1} {2} < {3} 2>&1".format(settings.SENDMAIL_BIN, sender.value, message.to_address, message.file_path())
                    output = subprocess.check_output(command, shell=True)
                    message.released = True
                    message.save()
                    response.append({ 'id':message_id, 'command': command, 'output': output })
                elif not settings.API_ONLY:
                    token = Token.objects.get(user=request.user)
                    host = MailScannerHost.objects.get(hostname=message.mailscanner_hostname)
                    protocol = 'https' if host.use_tls else 'http'
                    url = '{0}://{1}/api/messages/release/'.format(protocol, host.hostname)
                    headers = {
                        'Content-Type' : 'application/json',
                        'Authorization' : 'Token {0}'.format(token.key)
                    }
                    result = requests.post(url, json={ "messages": [message_id]}, headers=headers)
                    data = result.json()
                    if 'error' in data:
                        response.append({'id': data.['result'][0].id, 'error': data.['result'][0].error})
                    else:
                        response.append({'id': data.['result'][0].id, 'command': data.['result'][0].command, 'output': data.['result'][0].output})
                else:
                    response.append({'id': message_id, 'error': 'You are not authorized to run this request, as this node is for API requests only'})
            except Exception as e:
                response.append({'id': message_id, 'error': e})
            
        return Response({ 'result': response }, status=status.HTTP_200_OK)
        

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated], url_path='mark-spam', url_name='message-action-mark-spam')
    def post_action_spam(self, request):
        if not 'messages' in request.data:
            return Response({'error': 'No messages to process'}, status=status.HTTP_400_BAD_REQUEST)
        # Here we need to instruct the local MTA
        # to resend the message for the intended
        # recipient or an alternate recipient
        # sendmail -i -f REPLY_TO_ADDRESS TO_ADDRESS < FILEPATH_TO_MESSAGE 2>&1
        response = []
        sender = Setting.objects.get(key='mail.release.sender')
        for message_id in request.data['messages']:
            try:
                message = Message.objects.get(id=message_id)
                if settings.APP_HOSTNAME == message.mailscanner_hostname:
                    command = "{0} -p {1} -r {2}".format(settings.SA_BIN, settings.MAILSCANNER_CONFIG_DIR + '/spamassassin.conf', message.file_path())
                    output = subprocess.check_output(command, shell=True)
                    response.append({ 'id':message_id, 'command': command, 'output': output })
                elif not settings.API_ONLY:
                    token = Token.objects.get(user=request.user)
                    host = MailScannerHost.objects.get(hostname=message.mailscanner_hostname)
                    protocol = 'https' if host.use_tls else 'http'
                    url = '{0}://{1}/api/messages/mark-spam/'.format(protocol, host.hostname)
                    headers = {
                        'Content-Type' : 'application/json',
                        'Authorization' : 'Token {0}'.format(token.key)
                    }
                    result = requests.post(url, json={ "messages": [message_id]}, headers=headers)
                    data = result.json()
                    if 'error' in data:
                        response.append({'id': data.['result'][0].id, 'error': data.['result'][0].error})
                    else:
                        response.append({'id': data.['result'][0].id, 'command': data.['result'][0].command, 'output': data.['result'][0].output})
                else:
                    response.append({'id': message_id, 'error': 'You are not authorized to run this request, as this node is for API requests only'})
            except Exception as e:
                response.append({'id': message_id, 'error': e})
        return Response({ 'result': response }, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated], url_path='mark-nonspam', url_name='message-action-mark-nonspam')
    def post_action_nonspam(self, request):
        if not 'messages' in request.data:
            return Response({'error': 'No messages to process'}, status=status.HTTP_400_BAD_REQUEST)
        # Here we need to instruct the local MTA
        # to resend the message for the intended
        # recipient or an alternate recipient
        # sendmail -i -f REPLY_TO_ADDRESS TO_ADDRESS < FILEPATH_TO_MESSAGE 2>&1
        response = []
        sender = Setting.objects.get(key='mail.release.sender')
        for message_id in request.data['messages']:
            try:
                message = Message.objects.get(id=message_id)
                if settings.APP_HOSTNAME == message.mailscanner_hostname:
                    command = "{0} -p {1} -k {2}".format(settings.SA_BIN, settings.MAILSCANNER_CONFIG_DIR + '/spamassassin.conf', message.file_path())
                    output = subprocess.check_output(command, shell=True)
                    response.append({ 'id':message_id, 'command': command, 'output': output })
                elif not settings.API_ONLY:
                    token = Token.objects.get(user=request.user)
                    host = MailScannerHost.objects.get(hostname=message.mailscanner_hostname)
                    protocol = 'https' if host.use_tls else 'http'
                    url = '{0}://{1}/api/messages/mark-spam/'.format(protocol, host.hostname)
                    headers = {
                        'Content-Type' : 'application/json',
                        'Authorization' : 'Token {0}'.format(token.key)
                    }
                    result = requests.post(url, json={ "messages": [message_id]}, headers=headers)
                    data = result.json()
                    if 'error' in data:
                        response.append({'id': data.['result'][0].id, 'error': data.['result'][0].error})
                    else:
                        response.append({'id': data.['result'][0].id, 'command': data.['result'][0].command, 'output': data.['result'][0].output})
                else:
                    response.append({'id': message_id, 'error': 'You are not authorized to run this request, as this node is for API requests only'})
            except Exception as e:
                response.append({'id': message_id, 'error': e})
        return Response({ 'result': response }, status=status.HTTP_200_OK)

class HeaderViewSet(viewsets.ModelViewSet):
    queryset = Headers.objects.all()
    serializer_class = HeaderSerializer
    model = Headers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(HeaderViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return qs
        domains = [domain.name for domain in self.request.user.domains.all()]
        qs = qs.filter(Q(message__from_domain__in=domains) | Q(message__to_domain__in=domains))
        return qs

class SpamReportViewSet(viewsets.ModelViewSet):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    model = SpamReport
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(SpamReportViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return qs
        domains = [domain.name for domain in self.request.user.domains.all()]
        qs = qs.filter(Q(message__from_domain__in=domains) | Q(message__to_domain__in=domains))
        return qs

class RblReportViewSet(viewsets.ModelViewSet):
    queryset = RblReport.objects.all()
    serializer_class = RblReportSerializer
    model = RblReport
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(RblReportViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return qs
        domains = [domain.name for domain in self.request.user.domains.all()]
        qs = qs.filter(Q(message__from_domain__in=domains) | Q(message__to_domain__in=domains))
        return qs

class MailscannerReportViewSet(viewsets.ModelViewSet):
    queryset = MailscannerReport.objects.all()
    serializer_class = MailscannerReportSerializer
    model = MailscannerReport
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(MailscannerReportViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return qs
        domains = [domain.name for domain in self.request.user.domains.all()]
        qs = qs.filter(Q(message__from_domain__in=domains) | Q(message__to_domain__in=domains))
        return qs

class McpReportViewSet(viewsets.ModelViewSet):
    queryset = McpReport.objects.all()
    serializer_class = McpReportSerializer
    model = McpReport
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(McpReportViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return qs
        domains = [domain.name for domain in self.request.user.domains.all()]
        qs = qs.filter(Q(message__from_domain__in=domains) | Q(message__to_domain__in=domains))
        return qs



class TransportLogViewSet(viewsets.ModelViewSet):
    queryset = TransportLog.objects.all()
    serializer_class = TransportLogSerializer
    model = TransportLog
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(TransportLogViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return qs
        domains = [domain.name for domain in self.request.user.domains.all()]
        qs = qs.filter(Q(message__from_domain__in=domains) | Q(message__to_domain__in=domains))
        return qs

class SmtpRelayViewSet(viewsets.ModelViewSet):
    queryset = SmtpRelay.objects.all()
    serializer_class = SmtpRelaySerializer
    model = SmtpRelay
    permission_classes = (IsAdminUser,)