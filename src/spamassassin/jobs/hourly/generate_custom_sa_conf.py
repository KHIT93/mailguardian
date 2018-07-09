from django_extensions.management.jobs import HourlyJob
from spamassassin.models import Rule
from django.conf import settings
import os

class Job(HourlyJob):
    help = 'Hourly job to automatically regenerate the configuration/SpamAssassin/rules.spamassassin.conf file'

    def execute(self):
        contents = []
        for rule in Rule.objects.all():
            contents.append('score {0} {1}\n'.format(rule.name, rule.score))
        with open(os.path.join(settings.CONF_DIR, 'SpamAssassin', 'rules.spamassassin.conf'), 'w') as f:
            f.writelines(contents)