from rest_framework import serializers
from .models import ListEntry

class ListEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ListEntry
        fields = ('id', 'url', 'from_address', 'to_address', 'listing_type')
        
    # def validate_from_address(self, value):
    #     if '@' in value:
    #         raise serializers.ValidationError("You should only put the information that is in front of the @ symbol in this field")
    #     return value
    # def validate_from_domain(self, value):
    #     if '@' in value:
    #         raise serializers.ValidationError("You should only put the domain name, which is the part after the @ symbol, in this field")
    #     if '*' in value and not self.request.user.is_staff:
    #         raise serializers.ValidationError("Only Administrators/Staff is allowed to add wildcard domains to the list")
    #     return value

    # def validate_to_address(self, value):
    #     if '@' in value:
    #         raise serializers.ValidationError("You should only put the information that is in front of the @ symbol in this field")
    #     return value
    # def validate_to_domain(self, value):
    #     if '@' in value:
    #         raise serializers.ValidationError("You should only put the domain name, which is the part after the @ symbol, in this field")
    #     if '*' in value and not self.request.user.is_staff:
    #         raise serializers.ValidationError("Only Administrators/Staff is allowed to add wildcard domains to the list")
    #     return value
