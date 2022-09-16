from django.core.management.base import BaseCommand
from crontab import CronTab
from django.conf import settings
from subprocess import check_output
from core.helpers import which
import os
from django.utils.translation import gettext_lazy as _
from pathlib import Path

class Command(BaseCommand):
    help = _('Configure application cron jobs')

    def handle(self, *args, **kwargs):
        #user = check_output(which('whoami'), shell=True).decode('utf-8').replace(' ', '').replace('\n', ' ').replace('\r', '')
        cron = CronTab(user=True)
        job_hour = cron.new(command='{0} {1} runjobs hourly > /dev/null 2>&1'.format(which('python'), Path(settings.BASE_DIR, 'manage.py')))
        job_hour.every().hours()
        job_day = cron.new(command='{0} {1} runjobs daily > /dev/null 2>&1'.format(which('python'), Path(settings.BASE_DIR, 'manage.py')))
        job_day.every().day()
        job_week = cron.new(command='{0} {1} runjobs weekly > /dev/null 2>&1'.format(which('python'), Path(settings.BASE_DIR, 'manage.py')))
        job_week.setall('@weekly')
        job_month = cron.new(command='{0} {1} runjobs monthly > /dev/null 2>&1'.format(which('python'), Path(settings.BASE_DIR, 'manage.py')))
        job_month.every().month()
        cron.write()
        print(_('Cron jobs have been configured'))