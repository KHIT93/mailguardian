from django.db.models import Q
import abc

class QuerySetFilter:
    @abc.abstractmethod
    def filter(self, qs, filters):
        pass

class MessageQuerySetFilter(QuerySetFilter):
    def filter(self, qs, filters):
        if 'from_address' in filters:
            if filters['from_address']['operator'] == '=':
                qs = qs.filter(from_address__iexact=filters['from_address']['value'])
            elif filters['from_address']['operator'] == '<>':
                qs = qs.filter(~Q(from_address__iexact=filters['from_address']['value']))
            elif filters['from_address']['operator'] == 'icontains':
                qs = qs.filter(from_address__icontains=filters['from_address']['value'])
        
        if 'from_domain' in filters:
            if filters['from_domain']['operator'] == '=':
                qs = qs.filter(from_domain__iexact=filters['from_domain']['value'])
            elif filters['from_domain']['operator'] == '<>':
                qs = qs.filter(~Q(from_domain__iexact=filters['from_domain']['value']))
            elif filters['from_domain']['operator'] == 'icontains':
                qs = qs.filter(from_domain__icontains=filters['from_domain']['value'])
        
        if 'to_address' in filters:
            if filters['to_address']['operator'] == '=':
                qs = qs.filter(to_address__iexact=filters['to_address']['value'])
            elif filters['to_address']['operator'] == '<>':
                qs = qs.filter(~Q(to_address__iexact=filters['to_address']['value']))
            elif filters['to_address']['operator'] == 'icontains':
                qs = qs.filter(to_address__icontains=filters['to_address']['value'])
        
        if 'to_domain' in filters:
            if filters['to_domain']['operator'] == '=':
                qs = qs.filter(to_domain__iexact=filters['to_domain']['value'])
            elif filters['to_domain']['operator'] == '<>':
                qs = qs.filter(~Q(to_domain__iexact=filters['to_domain']['value']))
            elif filters['to_domain']['operator'] == 'icontains':
                qs = qs.filter(to_domain__icontains=filters['to_domain']['value'])

        if 'subject' in filters:
            if filters['subject']['operator'] == '=':
                qs = qs.filter(subject__iexact=filters['subject']['value'])
            elif filters['subject']['operator'] == '<>':
                qs = qs.filter(~Q(subject__iexact=filters['subject']['value']))
            elif filters['subject']['operator'] == 'icontains':
                qs = qs.filter(subject__icontains=filters['subject']['value'])
        
        if 'client_ip' in filters:
            if filters['client_ip']['operator'] == '=':
                qs = qs.filter(client_ip__iexact=filters['client_ip']['value'])
            elif filters['client_ip']['operator'] == '<>':
                qs = qs.filter(~Q(client_ip__iexact=filters['client_ip']['value']))

        if 'mailscanner_hostname' in filters:
            if filters['mailscanner_hostname']['operator'] == '=':
                qs = qs.filter(mailscanner_hostname__iexact=filters['mailscanner_hostname']['value'])
            elif filters['mailscanner_hostname']['operator'] == '<>':
                qs = qs.filter(~Q(mailscanner_hostname__iexact=filters['mailscanner_hostname']['value']))

        if 'date' in filters:
            if filters['date']['operator'] == '=':
                qs = qs.filter(date=filters['date']['value'])
            elif filters['date']['operator'] == '<>':
                qs = qs.filter(~Q(date=filters['date']['value']))
            elif filters['date']['operator'] == 'gt':
                qs = qs.filter(date__gt=filters['date']['value'])
            elif filters['date']['operator'] == 'gte':
                qs = qs.filter(date__gte=filters['date']['value'])
            elif filters['date']['operator'] == 'lt':
                qs = qs.filter(date__lt=filters['date']['value'])
            elif filters['date']['operator'] == 'lte':
                qs = qs.filter(date__lte=filters['date']['value'])

        if 'whitelisted' in filters:
            if filters['whitelisted']['operator'] == 1:
                qs = qs.filter(whitelisted__exact=True)
            if filters['whitelisted']['operator'] == 0:
                qs = qs.filter(whitelisted__exact=False)
        
        if 'blacklisted' in filters:
            if filters['blacklisted']['operator'] == 1:
                qs = qs.filter(blacklisted__exact=True)
            if filters['blacklisted']['operator'] == 0:
                qs = qs.filter(blacklisted__exact=False)

        if 'is_spam' in filters:
            if filters['is_spam']['operator'] == 1:
                qs = qs.filter(is_spam__exact=True)
            if filters['is_spam']['operator'] == 0:
                qs = qs.filter(is_spam__exact=False)

        if 'is_rbl_listed' in filters:
            if filters['is_rbl_listed']['operator'] == 1:
                qs = qs.filter(is_rbl_listed__exact=True)
            if filters['is_rbl_listed']['operator'] == 0:
                qs = qs.filter(is_rbl_listed__exact=False)

        if 'quarantined' in filters:
            if filters['quarantined']['operator'] == 1:
                qs = qs.filter(quarantined__exact=True)
            if filters['quarantined']['operator'] == 0:
                qs = qs.filter(quarantined__exact=False)

        if 'infected' in filters:
            if filters['infected']['operator'] == 1:
                qs = qs.filter(infected__exact=True)
            if filters['infected']['operator'] == 0:
                qs = qs.filter(infected__exact=False)

        return qs