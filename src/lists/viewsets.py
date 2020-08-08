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
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_domain__icontains=self.request.user.email.split('@')[-1]) | Q(to_domain__icontains=self.request.user.email.split('@')[-1]))
        return qs

class BlocklistEntryViewSet(ListEntryViewSet):
    queryset = ListEntry.objects.filter(listing_type='blocked')

class AllowlistEntryViewSet(ListEntryViewSet):
    queryset = ListEntry.objects.filter(listing_type='allowed')
