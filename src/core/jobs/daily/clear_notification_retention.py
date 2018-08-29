from django_extensions.management.jobs import DailyJob
from core.models import ApplicationNotification
from datetime import datetime, timedelta
from django.conf import settings

class Job(DailyJob):
    help = 'Daily database maintenance to remove auditlog.models.LogEntry entries that have passed the retention policy days'

    def execute(self):
        multi_node = True if host_count > 0 else False
        if (multi_node and not settings.API_ONLY) or not multi_node:
            to_remove = ApplicationNotification.objects.filter(date_end__lt=datetime.today() - timedelta(days=settings.RECORD_RETENTION))
            to_remove.delete()