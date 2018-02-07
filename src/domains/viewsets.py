from mailware.pagination import PageNumberPaginationWithPageCount
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import DomainSerializer, MailUserSerializer
from .models import Domain, MailUser

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    model = Domain
    pagination_class = PageNumberPaginationWithPageCount
    permission_classes = (IsAdminUser,)

class MailUserViewSet(viewsets.ModelViewSet):
    queryset = MailUser.objects.all()
    serializer_class = MailUserSerializer
    model = MailUser
    pagination_class = PageNumberPaginationWithPageCount
    permission_classes = (IsAdminUser,)