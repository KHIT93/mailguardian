from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Q
from .models import ListEntry
from .serializers import ListEntrySerializer

class ListEntryViewSet(viewsets.ModelViewSet):
    queryset = ListEntry.objects.all()
    serializer_class = ListEntrySerializer
    model = ListEntry
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.query_params.__contains__('search'):
            search_key = self.request.query_params.get('search')
            return self.queryset.filter(
                    Q(from_address__icontains=search_key) | Q(to_address__icontains=search_key)
                )
        else:
            return self.queryset

class BlacklistEntryViewSet(ListEntryViewSet):
    queryset = ListEntry.objects.filter(listing_type='blacklisted')

class WhitelistEntryViewSet(ListEntryViewSet):
    queryset = ListEntry.objects.filter(listing_type='whitelisted')
