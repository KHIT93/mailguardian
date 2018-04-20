from .models import Message, Headers, SpamReport, RblReport, McpReport, MailscannerReport
from rest_framework import serializers

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
            'whitelisted',
            'blacklisted',
            'is_spam',
            'is_rbl_listed',
            'quarantined',
            'infected',
            'queue_file_exists'
            )
    queue_file_exists = serializers.SerializerMethodField()
    mailq_path = serializers.SerializerMethodField()

    def get_queue_file_exists(self, obj):
        return obj.queue_file_exists()
    
    def get_mailq_path(self, obj):
        return obj.file_path()

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
        if not obj.contents == None:
            raw = obj.contents.replace('not spam, ', '').replace('spam, ', '').replace('SpamAssassin (', '').replace('not cached, ', '').replace(')', '').replace('autolearn=', '').split(', ')
            print(obj.id)
            del(raw[1])
            del(raw[0])
            for r in raw:
                if not r.startswith('required'):
                    try:
                        key, value = r.split(' ')
                        report[key] = value
                    except:
                        pass
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

    class Meta:
        fields = ('qid', 'size', 'parsed', 'parse_error', 'data', 'status', 'sender', 'recipients', 'errors')

class PostqueueStoreSerializer(serializers.Serializer):
    mails = PostqueueStoreMailSerializer(many=True, read_only=True)
    loaded_at = serializers.DateTimeField()

    class Meta:
        fields = ('mails', 'loaded_at')

