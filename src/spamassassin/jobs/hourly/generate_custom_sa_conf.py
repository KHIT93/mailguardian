from django_extensions.management.jobs import HourlyJob
from spamassassin.models import Rule
from django.conf import settings
import os
from django.utils.translation import gettext_lazy as _
from pathlib import Path

class Job(HourlyJob):
    help = 'Hourly job to automatically regenerate the configuration/SpamAssassin/rules.spamassassin.conf file'

    def execute(self):
        contents = []
        for rule in Rule.objects.all():
            contents.append('score {0} {1}\n'.format(rule.name, rule.score))
        with open(Path(settings.CONF_DIR, 'SpamAssassin', 'rules.spamassassin.conf'), 'w') as f:
            f.writelines(contents)