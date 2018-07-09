from .models import RuleDescription, Rule
from core.models import Setting
from .serializers import RuleDescriptionSerializer, RuleSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
import datetime

class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    model = Rule
    permission_classes = (IsAdminUser,)

class RuleDescriptionViewSet(viewsets.ModelViewSet):
    queryset = RuleDescription.objects.all()
    serializer_class = RuleDescriptionSerializer
    model = RuleDescription
    permission_classes = (IsAdminUser,)

    @action(methods=['post'], detail=False, permission_classes=[IsAdminUser], url_path='sync', url_name='sync-rule-descriptions')
    def post_sync_rule_descriptions(self, request):
        try:
            sa = RuleDescription()
            sa.sync_files()
            Setting.objects.update_or_create(key='sa.last_updated', defaults={'value':str(datetime.datetime.now())})
        except Exception as e:
            return Response({'message' : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, permission_classes=[IsAdminUser], url_path='all', url_name='all-rule-descriptions')
    def get_all(self, request):
        serializer = RuleDescriptionSerializer(self.get_queryset(), many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False, permission_classes=[IsAdminUser], url_path='available', url_name='available-rule')
    def get_available(self, request):
        current_rules = [rule.name for rule in Rule.objects.all()]
        qs = self.get_queryset()
        qs = qs.filter(~Q(key__in=current_rules))
        serializer = RuleDescriptionSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)