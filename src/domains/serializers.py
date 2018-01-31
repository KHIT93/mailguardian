from rest_framework import serializers
from .models import Domain

class DomainSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Domain
        fields = ('id', 'url', 'domain', 'destination', 'relay_destination', 'relay_type' ,'created_timestamp' ,'updated_timestamp', 'active', 'allowed_accounts')