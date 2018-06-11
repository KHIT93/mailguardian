from mailguardian.pagination import PageNumberPaginationWithPageCount
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import DomainSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Domain

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    model = Domain
    pagination_class = PageNumberPaginationWithPageCount
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        qs = super(DomainViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return qs
        domains = [domain.name for domain in self.request.user.domains.all()]
        qs = qs.filter(name__in=domains)
        return qs

    @action(methods=['get'], detail=False, permission_classes=[IsAdminUser], url_path='all', url_name='all-domains')
    def get_all(self, request):
        serializer = DomainSerializer(self.get_queryset(), many=True, context={'request': request})
        return Response(serializer.data)