from rest_framework import viewsets
from django.db.models import Q
from .models import ListEntry
from .serializers import ListEntrySerializer

class ListEntryViewSet(viewsets.ModelViewSet):
    queryset = ListEntry.objects.all()
    serializer_class = ListEntrySerializer
    model = ListEntry

    def get_queryset(self):
        if self.request.query_params.__contains__('search'):
            search_key = self.request.query_params.get('search')
            return self.queryset.filter(
                    Q(from_address__icontains=search_key) | Q(from_domain__icontains=search_key) | Q(from_ip_address__icontains=search_key) |
                    Q(to_address__icontains=search_key) | Q(to_domain__icontains=search_key) | Q(to_ip_address__icontains=search_key)
                )
        else:
            return ListEntry.objects.all()

class BlacklistEntryViewSet(ListEntryViewSet):
    queryset = ListEntry.objects.filter(listing_type='blacklisted')

class WhitelistEntryViewSet(ListEntryViewSet):
    queryset = ListEntry.objects.filter(listing_type='whitelisted')
