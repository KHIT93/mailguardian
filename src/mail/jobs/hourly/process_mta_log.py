from django_extensions.management.jobs import HourlyJob
from .models import Message
from datetime import datetime, timedelta
from django.conf import settings
from mail.log_processors import PostfixLogProcessor

class Job(HourlyJob):
    help = 'Hourly job to read the logfile of the MTA and add the log entry to mail.models.TransportLog'

    def execute(self):
        mta_log_processor = PostfixLogProcessor()
        mta_log_processor.execute()