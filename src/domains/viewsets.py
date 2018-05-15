from mailware.pagination import PageNumberPaginationWithPageCount
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import DomainSerializer
from .models import Domain

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    model = Domain
    pagination_class = PageNumberPaginationWithPageCount
    permission_classes = (IsAdminUser,)