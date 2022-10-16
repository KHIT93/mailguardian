from django.db.models import Q
import abc

VALID_FILTERS = {
    'from_address': {
        'label': 'Sender',
        'autocomplete': 'email',
        'operators': [
            { 'label': 'equals', 'value': '=' },
            { 'label': 'does not equal', 'value': '<>' },
            { 'label': 'contains', 'value': 'icontains' }
        ],
        'field_type': 'text'
    },
    'from_domain': {
        'label': 'Sender Domain',
        'autocomplete': 'text',
        'operators': [
            { 'label': 'equals', 'value': '=' },
            { 'label': 'does not equal', 'value': '<>' },
            { 'label': 'contains', 'value': 'icontains' }
        ],
        'field_type': 'text'
    },
    'to_address': {
        'label': 'Recipient',
        'autocomplete': 'email',
        'operators': [
            { 'label': 'equals', 'value': '=' },
            { 'label': 'does not equal', 'value': '<>' },
            { 'label': 'contains', 'value': 'icontains' }
        ],
        'field_type': 'text'
    },
    'to_domain': {
        'label': 'Recipient Domain',
        'autocomplete': 'text',
        'operators': [
            { 'label': 'equals', 'value': '=' },
            { 'label': 'does not equal', 'value': '<>' },
            { 'label': 'contains', 'value': 'icontains' }
        ],
        'field_type': 'text'
    },
    'subject': {
        'label': 'Subject',
        'autocomplete': 'text',
        'operators': [
            { 'label': 'equals', 'value': '=' },
            { 'label': 'does not equal', 'value': '<>' },
            { 'label': 'contains', 'value': 'icontains' }
        ],
        'field_type': 'text'
    },
    'client_ip': {
        'label': 'Sender IP-address',
        'autocomplete': 'off',
        'operators': [
            { 'label': 'equals', 'value': '=' },
            { 'label': 'does not equal', 'value': '<>' }
        ],
        'field_type': 'text'
    },
    'mailscanner_hostname': {
        'label': 'MailScanner Host',
        'autocomplete': 'text',
        'operators': [
            { 'label': 'equals', 'value': '=' },
            { 'label': 'does not equal', 'value': '<>' }
        ],
        'field_type': 'text'
    },
    'date': {
        'label': 'Date',
        'autocomplete': 'off',
        'operators': [
            { 'label': 'equals', 'value': '=' },
            { 'label': 'does not equal', 'value': '<>' },
            { 'label': 'greater than', 'value': 'gt' },
            { 'label': 'greater than or equals', 'value': 'gte' },
            { 'label': 'less than', 'value': 'lt'},
            { 'label': 'less than or equals', 'value': 'lte'}
        ],
        'field_type': 'date'
    },
    'allowed': {
        'label': 'Allowed',
        'operators': [
            { 'label': 'yes', 'value': 1},
            { 'label': 'no', 'value': 0}
        ],
        'field_type': 'boolean'
    },
    'blocked': {
        'label': 'Blocked',
        'operators': [
            { 'label': 'yes', 'value': 1},
            { 'label': 'no', 'value': 0}
        ],
        'field_type': 'boolean'
    },
    'is_spam': {
        'label': 'Marked as SPAM',
        'operators': [
            { 'label': 'yes', 'value': 1},
            { 'label': 'no', 'value': 0}
        ],
        'field_type': 'boolean'
    },
    'is_rbl_listed': {
        'label': 'Listed in RBL',
        'operators': [
            { 'label': 'yes', 'value': 1},
            { 'label': 'no', 'value': 0}
        ],
        'field_type': 'boolean'
    },
    'stored': {
        'label': 'Stored',
        'operators': [
            { 'label': 'yes', 'value': 1},
            { 'label': 'no', 'value': 0}
        ],
        'field_type': 'boolean'
    },
    'infected': {
        'label': 'Infected',
        'operators': [
            { 'label': 'yes', 'value': 1},
            { 'label': 'no', 'value': 0}
        ],
        'field_type': 'boolean'
    }
}

class QuerySetFilter:
    @abc.abstractmethod
    def filter(self, qs, filters, user):
        pass

class MessageQuerySetFilter(QuerySetFilter):
    def filter(self, qs, filters, user):
        domains = [domain.name for domain in user.domains.all()]
        allow_from_filter = False
        allow_to_filter = False
        if user.is_staff:
            allow_from_filter = True
            allow_to_filter = True
        elif user.is_domain_admin:
            if 'to_address' in filters or 'to_domain' in filters:
                if ('to_address' in filters and filters['to_address']['value'].split('@')[-1] in domains) or ('to_domain' in filters and filters['to_domain']['value'] in domains):
                    allow_to_filter = True
                    allow_from_filter = False
                else:
                    allow_to_filter = True
                    qs = qs.filter(from_domain__in=domains)
            elif 'from_address' in filters or'from_domain' in filters:
                if ('from_address' in filters and filters['from_address']['value'].split('@')[-1] in domains) or ('from_domain' in filters and filters['from_domain']['value'] in domains):
                    allow_to_filter = False
                    allow_from_filter = True
                else:
                    allow_from_filter = True
                    qs = qs.filter(to_domain__in=domains)
            else:
                qs = qs.filter(Q(from_domain__in=domains) | Q(to_domain__in=domains))
        else:
            if ('to_address' in filters and filters['to_address']['value'] != user.email) or 'to_domain' in filters:
                allow_to_filter = True
                allow_from_filter = False
                qs = qs.filter(from_address=user.email)
            elif ('from_address' in filters and filters['from_address']['value'] != user.email) or 'from_domain' in filters:
                allow_to_filter = False
                allow_from_filter = True
                qs = qs.filter(to_address=user.email)
            else:
                qs = qs.filter(Q(from_address=user.email) | Q(to_address=user.email))

        if 'from_address' in filters and allow_from_filter:
            if filters['from_address']['operator'] == '=':
                qs = qs.filter(from_address__iexact=filters['from_address']['value'])
            elif filters['from_address']['operator'] == '<>':
                qs = qs.filter(~Q(from_address__iexact=filters['from_address']['value']))
            elif filters['from_address']['operator'] == 'icontains':
                qs = qs.filter(from_address__icontains=filters['from_address']['value'])
        
        if 'from_domain' in filters and allow_from_filter:
            if filters['from_domain']['operator'] == '=':
                qs = qs.filter(from_domain__iexact=filters['from_domain']['value'])
            elif filters['from_domain']['operator'] == '<>':
                qs = qs.filter(~Q(from_domain__iexact=filters['from_domain']['value']))
            elif filters['from_domain']['operator'] == 'icontains':
                qs = qs.filter(from_domain__icontains=filters['from_domain']['value'])
        
        if 'to_address' in filters and allow_to_filter:
            if filters['to_address']['operator'] == '=':
                qs = qs.filter(to_address__iexact=filters['to_address']['value'])
            elif filters['to_address']['operator'] == '<>':
                qs = qs.filter(~Q(to_address__iexact=filters['to_address']['value']))
            elif filters['to_address']['operator'] == 'icontains':
                qs = qs.filter(to_address__icontains=filters['to_address']['value'])
        
        if 'to_domain' in filters and allow_to_filter:
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

        if 'allowed' in filters:
            if filters['allowed']['operator'] == 1:
                qs = qs.filter(allowed__exact=True)
            if filters['allowed']['operator'] == 0:
                qs = qs.filter(allowed__exact=False)
        
        if 'blocked' in filters:
            if filters['blocked']['operator'] == 1:
                qs = qs.filter(blocked__exact=True)
            if filters['blocked']['operator'] == 0:
                qs = qs.filter(blocked__exact=False)

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