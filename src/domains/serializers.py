from rest_framework import serializers
from .models import Domain, MailUser

class DomainSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Domain
        fields = ('id', 'url', 'name', 'destination', 'relay_type' ,'created_timestamp' ,'updated_timestamp', 'active', 'allowed_accounts')

class MailUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailUser
        fields = ('id', 'url', 'domain', 'domain_id', 'is_domain_admin')

    domain_id = serializers.PrimaryKeyRelatedField(read_only=True)