from django.contrib.auth.models import User
from rest_framework import serializers
from domains.serializers import MailUserSerializer
from .models import MailScannerConfiguration

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'is_staff', 'first_name', 'last_name', 'full_name', 'mailuser')

    full_name = serializers.SerializerMethodField()
    mailuser = MailUserSerializer(many=False, read_only=True)

    def get_full_name(self, obj):
        if obj.first_name != "" and obj.last_name != "":
            return obj.first_name + " " + obj.last_name
        else:
            return obj.username

class MailScannerConfigurationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailScannerConfiguration
        fields = ('id', 'url', 'key', 'value', 'filepath')