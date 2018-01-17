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
            return obj.from_address + "@" + obj.from_domain
        elif not obj.from_domain == "":
            return "@" + obj.from_domain
        elif not obj.from_ip_address == "":
            return obj.from_ip_address
        else:
            return ""

    def get__to(self, obj):
        if not obj.to_address == "":
            return obj.to_address + "@" + obj.to_domain
        elif not obj.to_domain == "":
            return "@" + obj.to_domain
        elif not obj.to_ip_address == "":
            return obj.to_ip_address
        else:
            return ""
        
    def validate_from_address(self, value):
        if '@' in value:
            raise serializers.ValidationError("You should only put the information that is in front of the @ symbol in this field")
        return value
    def validate_from_domain(self, value):
        if '@' in value:
            raise serializers.ValidationError("You should only put the domain name, which is the part after the @ symbol, in this field")
        if '*' in value and not self.request.user.is_staff:
            raise serializers.ValidationError("Only Administrators/Staff is allowed to add wildcard domains to the list")
        return value

    def validate_to_address(self, value):
        if '@' in value:
            raise serializers.ValidationError("You should only put the information that is in front of the @ symbol in this field")
        return value
    def validate_to_domain(self, value):
        if '@' in value:
            raise serializers.ValidationError("You should only put the domain name, which is the part after the @ symbol, in this field")
        if '*' in value and not self.request.user.is_staff:
            raise serializers.ValidationError("Only Administrators/Staff is allowed to add wildcard domains to the list")
        return value
