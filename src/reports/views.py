from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from mail.models import Message
from django.db.models import Q

class SummaryApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        data = request.data
        print(data)
        qs = Message.objects.all()
        if 'from_address' in data:
            if data['from_address']['operator'] == '=':
                qs = qs.filter(from_address__iexact=data['from_address']['value'])
            elif data['from_address']['operator'] == '<>':
                qs = qs.filter(~Q(from_address__iexact=data['from_address']['value']))
            elif data['from_address']['operator'] == 'icontains':
                qs = qs.filter(from_address__icontains=data['from_address']['value'])
        
        if 'from_domain' in data:
            if data['from_domain']['operator'] == '=':
                qs = qs.filter(from_domain__iexact=data['from_domain']['value'])
            elif data['from_domain']['operator'] == '<>':
                qs = qs.filter(~Q(from_domain__iexact=data['from_domain']['value']))
            elif data['from_domain']['operator'] == 'icontains':
                qs = qs.filter(from_domain__icontains=data['from_domain']['value'])
        
        if 'to_address' in data:
            if data['to_address']['operator'] == '=':
                qs = qs.filter(to_address__iexact=data['to_address']['value'])
            elif data['to_address']['operator'] == '<>':
                qs = qs.filter(~Q(to_address__iexact=data['to_address']['value']))
            elif data['to_address']['operator'] == 'icontains':
                qs = qs.filter(to_address__icontains=data['to_address']['value'])
        
        if 'to_domain' in data:
            if data['to_domain']['operator'] == '=':
                qs = qs.filter(to_domain__iexact=data['to_domain']['value'])
            elif data['to_domain']['operator'] == '<>':
                qs = qs.filter(~Q(to_domain__iexact=data['to_domain']['value']))
            elif data['to_domain']['operator'] == 'icontains':
                qs = qs.filter(to_domain__icontains=data['to_domain']['value'])

        if 'subject' in data:
            if data['subject']['operator'] == '=':
                qs = qs.filter(subject__iexact=data['subject']['value'])
            elif data['subject']['operator'] == '<>':
                qs = qs.filter(~Q(subject__iexact=data['subject']['value']))
            elif data['subject']['operator'] == 'icontains':
                qs = qs.filter(subject__icontains=data['subject']['value'])
        
        if 'client_ip' in data:
            if data['client_ip']['operator'] == '=':
                qs = qs.filter(client_ip__iexact=data['client_ip']['value'])
            elif data['client_ip']['operator'] == '<>':
                qs = qs.filter(~Q(client_ip__iexact=data['client_ip']['value']))

        if 'mailscanner_hostname' in data:
            if data['mailscanner_hostname']['operator'] == '=':
                qs = qs.filter(mailscanner_hostname__iexact=data['mailscanner_hostname']['value'])
            elif data['mailscanner_hostname']['operator'] == '<>':
                qs = qs.filter(~Q(mailscanner_hostname__iexact=data['mailscanner_hostname']['value']))

        if 'timestamp' in data:
            if data['timestamp']['operator'] == '=':
                qs = qs.filter(timestamp__iexact=data['timestamp']['value'])
            elif data['timestamp']['operator'] == '<>':
                qs = qs.filter(~Q(timestamp__iexact=data['timestamp']['value']))
            elif data['timestamp']['operator'] == 'gt':
                qs = qs.filter(timestamp__gt=data['timestamp']['value'])
            elif data['timestamp']['operator'] == 'gte':
                qs = qs.filter(timestamp__gte=data['timestamp']['value'])
            elif data['timestamp']['operator'] == 'lt':
                qs = qs.filter(timestamp__lt=data['timestamp']['value'])
            elif data['timestamp']['operator'] == 'lte':
                qs = qs.filter(timestamp__lte=data['timestamp']['value'])

        if 'whitelisted' in data:
            if data['whitelisted']['operator'] == 1:
                qs = qs.filter(whitelisted__exact=True)
            if data['whitelisted']['operator'] == 0:
                qs = qs.filter(whitelisted__exact=False)
        
        if 'blacklisted' in data:
            if data['blacklisted']['operator'] == 1:
                qs = qs.filter(blacklisted__exact=True)
            if data['blacklisted']['operator'] == 0:
                qs = qs.filter(blacklisted__exact=False)

        if 'is_spam' in data:
            if data['is_spam']['operator'] == 1:
                qs = qs.filter(is_spam__exact=True)
            if data['is_spam']['operator'] == 0:
                qs = qs.filter(is_spam__exact=False)

        if 'is_rbl_listed' in data:
            if data['is_rbl_listed']['operator'] == 1:
                qs = qs.filter(is_rbl_listed__exact=True)
            if data['is_rbl_listed']['operator'] == 0:
                qs = qs.filter(is_rbl_listed__exact=False)

        if 'quarantined' in data:
            if data['quarantined']['operator'] == 1:
                qs = qs.filter(quarantined__exact=True)
            if data['quarantined']['operator'] == 0:
                qs = qs.filter(quarantined__exact=False)

        if 'infected' in data:
            if data['infected']['operator'] == 1:
                qs = qs.filter(infected__exact=True)
            if data['infected']['operator'] == 0:
                qs = qs.filter(infected__exact=False)

        response_data = {
            'latest': qs.latest().timestamp,
            'earliest': qs.earliest().timestamp,
            'count': qs.count()
        }

        return Response(response_data, 200)