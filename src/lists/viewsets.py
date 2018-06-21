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
        qs = super(ListEntryViewSet, self).get_queryset()
        if self.request.query_params.__contains__('search'):
            search_key = self.request.query_params.get('search')
            qs = qs.filter(
                    Q(from_address__icontains=search_key) | Q(to_address__icontains=search_key)
                )
        if self.request.user.is_staff:
            return qs
        domains = [domain.name for domain in self.request.user.domains.all()]
        qs = qs.filter(to_domain__in=domains)
        return qs

class BlacklistEntryViewSet(ListEntryViewSet):
    queryset = ListEntry.objects.filter(listing_type='blacklisted')

class WhitelistEntryViewSet(ListEntryViewSet):
    queryset = ListEntry.objects.filter(listing_type='whitelisted')
