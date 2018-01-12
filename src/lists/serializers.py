from rest_framework import serializers
from .models import ListEntry

class ListEntrySerializer(serializers.HyperlinkedModelSerializer):
    _from = serializers.SerializerMethodField()
    _to = serializers.SerializerMethodField()
    class Meta:
        model = ListEntry
        fields = ('id', 'url', 'from_address', 'to_address', 'from_domain', 'to_domain', 'from_ip_address', 'to_ip_address', 'listing_type', '_from', '_to')

    def get__from(self, obj):
        if not obj.from_address == "":
            return obj.from_address
        elif not obj.from_domain == "":
            return "@" + obj.from_domain
        elif not obj.from_ip_address == "":
            return obj.from_ip_address
        else:
            return ""

    def get__to(self, obj):
        if not obj.to_address == "":
            return obj.to_address
        elif not obj.to_domain == "":
            return "@" + obj.to_domain
        elif not obj.to_ip_address == "":
            return obj.to_ip_address
        else:
            return ""
        