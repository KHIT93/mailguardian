from .models import Message, Headers, SpamReport, RblReport, McpReport, MailscannerReport, TransportLog, SmtpRelay
from rest_framework import serializers
from spamassassin.models import RuleDescription
import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Serializers define the API representation.
class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'url',
            'from_address',
            'from_domain',
            'to_address',
            'to_domain',
            'subject',
            'client_ip',
            'mailscanner_hostname',
            'spam_score',
            'timestamp',
            'date',
            'size',
            'token',
            'mailq_id',
            'mailq_path',
            'allowed',
            'blocked',
            'is_spam',
            'is_rbl_listed',
            'stored',
            'scanned',
            'infected',
            'is_clean'
            )
    mailq_path = serializers.SerializerMethodField()
    is_clean = serializers.SerializerMethodField()
    
    def get_mailq_path(self, obj):
        return obj.file_path()

    def get_is_clean(self, obj):
        if not obj.is_spam and not obj.is_rbl_listed and not obj.infected:
            return True
        else:
            return False

class HeaderSerializer(serializers.HyperlinkedModelSerializer):
    headers = serializers.SerializerMethodField()
    class Meta:
        model = Headers
        fields = ('id', 'url', 'message_id', 'headers')

    def get_headers(self, obj):
        raw = obj.contents.replace('\r\n\t', '').splitlines()
        headers = {}
        previous = ''
        for h in raw:
            data = h.split(': ', 1)
            if len(data) > 1:
                headers[data[0]] = data[1].replace('\r\n ', '\r\n')
                previous = data[0]
            else:
                headers[previous] += '\r\n' + data[0].replace(' ', '')
        return headers

class SpamReportSerializer(serializers.HyperlinkedModelSerializer):
    report = serializers.SerializerMethodField()
    class Meta:
        model = SpamReport
        fields = ('id', 'url', 'message_id', 'report')

    def get_report(self, obj):
        report = {}
        too_large = False
        if not obj.contents == None:
            raw = obj.contents.replace('not spam, ', '').replace('not spam (too large)', 'too large').replace('spam, ', '').replace('SpamAssassin (', '').replace('not cached, ', '').replace(')', '').replace('autolearn=', '').split(', ')
            if 'too large' in raw:
                too_large = True
            print(obj.id)
            if not too_large:
                del(raw[1])
            del(raw[0])
            for r in raw:
                if not r.startswith('required'):
                    try:
                        key, value = r.split(' ')
                        description = ''
                        try:
                            description = RuleDescription.objects.filter(key=key).first().value
                        except:
                            description = ''
                        report[key] = { 'value' : value, 'description': description }
                    except:
                        pass
            if too_large:
                report['TOO_LARGE'] = _('The message is too large to be scanned by SpamAssassin')
        return report

class RblReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RblReport
        fields = ('id', 'url', 'message_id', 'contents')

class MailscannerReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailscannerReport
        fields = ('id', 'url', 'message_id', 'contents')

class McpReportSerializer(serializers.HyperlinkedModelSerializer):
    report = serializers.SerializerMethodField()
    class Meta:
        model = McpReport
        fields = ('id', 'url', 'message_id', 'report')

    def get_report(self, obj):
        report = {}
        if not obj.contents == None:
            raw = obj.contents.replace('not spam, ', '').replace('spam, ', '').replace('SpamAssassin (', '').replace('not cached, ', '').replace(')', '').split(', ')
            del(raw[1])
            del(raw[0])
            for r in raw:
                try:
                    key, value = r.split(' ')
                    report[key] = value
                except:
                    pass
        return report

class MessageActionSerializer(serializers.Serializer):
    message_id = serializers.UUIDField()
    action = serializers.CharField(max_length=255)
    class Meta:
        fields = ('message_id', 'action')

class MessageContentsSerializer(serializers.Serializer):
    message_id = serializers.UUIDField()
    mailq_id = serializers.CharField()
    message_contents = serializers.CharField()
    class Meta:
        fields = ('mesage_id', 'mailq_id', 'message_contents')

class PostqueueStoreMailSerializer(serializers.Serializer):
    qid = serializers.CharField(max_length=255)
    size = serializers.FloatField()
    parsed = serializers.BooleanField()
    parse_error = serializers.CharField()
    date = serializers.DateTimeField()
    status = serializers.CharField()
    sender = serializers.CharField()
    recipients = serializers.ListField(child=serializers.CharField())
    errors = serializers.ListField(child=serializers.CharField())
    hostname = serializers.CharField(max_length=255, required=False)

    class Meta:
        fields = ('qid', 'size', 'parsed', 'parse_error', 'data', 'status', 'sender', 'recipients', 'errors', 'hostname')

class PostqueueStoreSerializer(serializers.Serializer):
    mails = PostqueueStoreMailSerializer(many=True, read_only=True)
    loaded_at = serializers.DateTimeField()

    class Meta:
        fields = ('mails', 'loaded_at')

class TransportLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TransportLog
        fields = ('id', 'url', 'message_id', 'timestamp', 'transport_host', 'transport_type', 'relay_host', 'dsn', 'dsn_message', 'delay')

class SmtpRelaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SmtpRelay
        fields = ('id', 'url', 'ip_address', 'hostname', 'active', 'comment')