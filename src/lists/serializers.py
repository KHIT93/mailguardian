from rest_framework import serializers
from .models import ListEntry
from django.utils.translation import gettext_lazy as _

class ListEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ListEntry
        fields = ('id', 'url', 'from_address', 'from_domain', 'to_address', 'to_domain', 'listing_type')
        
    def validate(self, data):
        current_user = self.context['request'].user
        qs = ListEntry.objects.filter(**data).exists()
        if not qs:
            raise serializers.ValidationError(_('A listing entry for this already exists'))
        if current_user.is_staff:
            return data
        elif current_user.is_domain_admin:
            domains = [domain.name for domain in current_user.domains.all()]
            from_domain = data['from_address'].split('@')[-1]
            to_domain = data['to_address'].split('@')[-1]
            if (from_domain in domains) or (to_domain in domains):
                return data
            elif current_user.email in [data['to_address'], data['from_address']]:
                return data
            else:
                raise serializers.ValidationError(_('You are only allowed to add entries for your own domains'))
        else:
            if current_user.email in [data['to_address'], data['from_address']]:
                return data
            else:
                raise serializers.ValidationError(_('You are not allowed to add entries for others than yourself'))

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
