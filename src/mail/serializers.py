from .models import Message, Headers, SpamReport, RblReport, McpReport
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
            'token',
            'whitelisted',
            'blacklisted',
            'is_spam',
            'is_rbl_listed',
            'quarantined',
            'infected'
            )

class HeaderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Headers
        fields = ('id', 'url', 'message_id', 'contents')

class SpamReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpamReport
        fields = ('id', 'url', 'message_id', 'contents')

class RblReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RblReport
        fields = ('id', 'url', 'message_id', 'contents')

class McpReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = McpReport
        fields = ('id', 'url', 'message_id', 'contents')