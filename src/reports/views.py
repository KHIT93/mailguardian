from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.db.models import Count, Sum, When, Case
from mail.models import Message
from mail.serializers import MessageSerializer
from reports.filters import MessageQuerySetFilter, VALID_FILTERS
from reports.serializers import MessagesByDateSerializer, MessageRelaysSerializer, MessagesPerHourSerializer, TopSendersByQuantitySerializer, TopSendersByVolumeSerializer, TopRecipientsByQuantitySerializer, TopRecipientsByVolumeSerializer, TopSenderDomainsByQuantitySerializer, TopSenderDomainsByVolumeSerializer, TopRecipientDomainsByQuantitySerializer, TopRecipientDomainsByVolumeSerializer
from mailguardian.pagination import PageNumberPaginationWithPageCount
import datetime
from django.db.models import Q

class SummaryApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs

    def post(self, request, format=None):
        filters = {}
        for filter in request.data:
            filters[filter['name']] = {
                'operator': filter['operator'],
                'value': filter.get('value', None)
            }
        response_data = {}
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset(), filters, request.user)
        try:
            response_data = {
                'latest': qs.latest().date,
                'earliest': qs.earliest().date,
                'count': qs.count()
            }
        except:
            response_data = {
                'latest': '',
                'earliest': '',
                'count': 0
            }
        return Response(response_data, 200)

class ValidFilterChoicesApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        formatted_filters = [
            {
                'name': key,
                'label': VALID_FILTERS[key]['label'],
                'operators': VALID_FILTERS[key]['operators'],
                'field_type': VALID_FILTERS[key]['field_type'],
                'autocomplete': VALID_FILTERS[key].get('autocomplete', False),
            } for key in VALID_FILTERS.keys()
        ]
        return Response(formatted_filters, status=status.HTTP_200_OK)

class MessageListApiView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPaginationWithPageCount

    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs
    
    def post(self, request, format=None):
        # filters = request.data
        # qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset(), filters, request.user)
        # print(len(qs))
        # self.queryset = qs
        return self.list(request)

    """
    List a queryset.
    Overrides rest_framework.mixins.ListModelMixin.list, as it recreates the queryset without our filters
    """
    def list(self, request, *args, **kwargs):
        filters = request.data
        queryset = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset(), filters, request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MessagesByDateApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs

    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset().values('date'), filters, request.user)
        serializer = MessagesByDateSerializer(qs.annotate(Count('id')).annotate(is_spam_count=Count(Case(When(is_spam=True, then=1)))).annotate(Sum('size')).annotate(infected_count=Count(Case(When(infected=True, then=1)))).order_by('date'), many=True)
        return Response(serializer.data, 200)

class TopMailRelaysApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs

    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset().values('client_ip'), filters, request.user)
        serializer = MessageRelaysSerializer(qs.annotate(Count('id')).annotate(is_spam_count=Count(Case(When(is_spam=True, then=1)))).annotate(Sum('size')).annotate(infected_count=Count(Case(When(infected=True, then=1)))).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)

class MessagesPerHourApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs
    
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset().values('timestamp').filter(timestamp__range=[datetime.datetime.now() - datetime.timedelta(days=1), datetime.datetime.now()]), filters, request.user)
        serializer = MessagesPerHourSerializer(qs.annotate(Count('id')).annotate(is_spam_count=Count(Case(When(is_spam=True, then=1)))).annotate(Sum('size')).annotate(infected_count=Count(Case(When(infected=True, then=1)))).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)

class TopSendersByQuantityApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs
    
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset().values('from_address'), filters, request.user)
        serializer = TopSendersByQuantitySerializer(qs.annotate(Count('id')).annotate(Sum('size')).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)

class TopSendersByVolumeApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs
    
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset().values('from_address'), filters, request.user)
        serializer = TopSendersByVolumeSerializer(qs.annotate(Count('id')).annotate(Sum('size')).order_by('-size__sum')[:10], many=True)
        return Response(serializer.data, 200)

class TopRecipientsByQuantityApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs
    
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset().values('to_address'), filters, request.user)
        serializer = TopRecipientsByQuantitySerializer(qs.annotate(Count('id')).annotate(Sum('size')).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)

class TopRecipientsByVolumeApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs
    
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset().values('to_address'), filters, request.user)
        serializer = TopRecipientsByVolumeSerializer(qs.annotate(Count('id')).annotate(Sum('size')).order_by('-size__sum')[:10], many=True)
        return Response(serializer.data, 200)

class TopSenderDomainsByQuantityApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs
    
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset().values('from_domain'), filters, request.user)
        serializer = TopSenderDomainsByQuantitySerializer(qs.annotate(Count('id')).annotate(Sum('size')).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)

class TopSenderDomainsByVolumeApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs
    
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset().values('from_domain'), filters, request.user)
        serializer = TopSenderDomainsByVolumeSerializer(qs.annotate(Count('id')).annotate(Sum('size')).order_by('-size__sum')[:10], many=True)
        return Response(serializer.data, 200)

class TopRecipientDomainsByQuantityApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs
    
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset().values('to_domain'), filters, request.user)
        serializer = TopRecipientDomainsByQuantitySerializer(qs.annotate(Count('id')).annotate(Sum('size')).order_by('-id__count')[:10], many=True)
        return Response(serializer.data, 200)

class TopRecipientDomainsByVolumeApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        qs = Message.objects.all()
        if self.request.user.is_staff:
            return qs
        elif self.request.user.is_domain_admin:
            domains = [domain.name for domain in self.request.user.domains.all()]
            qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            qs = qs.filter(Q(from_address=self.request.user.email) | Q(to_address=self.request.user.email))
        return qs
    
    def post(self, request, format=None):
        filters = request.data
        qs = MessageQuerySetFilter.filter(MessageQuerySetFilter, self.get_queryset().values('to_domain'), filters, request.user)
        serializer = TopRecipientDomainsByVolumeSerializer(qs.annotate(Count('id')).annotate(Sum('size')).order_by('-size__sum')[:10], many=True)
        return Response(serializer.data, 200)