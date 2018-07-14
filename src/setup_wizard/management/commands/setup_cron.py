from django.core.management.base import BaseCommand, CommandError
from crontab import CronTab
from django.conf import settings
from subprocess import check_output
from core.helpers import which
import os

class Command(BaseCommand):
    help = 'Configure application cron jobs'

    def handle(self, *args, **kwargs):
        #user = check_output(which('whoami'), shell=True).decode('utf-8').replace(' ', '').replace('\n', ' ').replace('\r', '')
        cron = CronTab(user=True)
        job_hour = cron.new(command='{0} {1} runjobs hourly'.format(which('python'), os.path.join(settings.BASE_DIR, 'src', 'manage.py')))
        job_hour.every().hours()
        job_day = cron.new(command='{0} {1} runjobs daily'.format(which('python'), os.path.join(settings.BASE_DIR, 'src', 'manage.py')))
        job_day.every().day()
        job_week = cron.new(command='{0} {1} runjobs weekly'.format(which('python'), os.path.join(settings.BASE_DIR, 'src', 'manage.py')))
        job_week.setall('@weekly')
        job_month = cron.new(command='{0} {1} runjobs monthly'.format(which('python'), os.path.join(settings.BASE_DIR, 'src', 'manage.py')))
        job_month.every().month()
        cron.write()
        print('Cron jobs have been configured')