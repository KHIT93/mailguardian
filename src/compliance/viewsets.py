from rest_framework import viewsets
from .models import DataLogEntry
from .serializers import DataLogEntrySerializer
from rest_framework.permissions import IsAdminUser

class DataLogEntryViewSet(viewsets.ModelViewSet):
    queryset = DataLogEntry.objects.all()
    serializer_class = DataLogEntrySerializer
    permission_classes = (IsAdminUser,)
    model = DataLogEntry

    def get_queryset(self):
        qs = super(DataLogEntryViewSet, self).get_queryset()
        return qs