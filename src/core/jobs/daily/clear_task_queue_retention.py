from django_extensions.management.jobs import DailyJob
from core.models import ApplicationTask
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Job(DailyJob):
    help = _('Daily database maintenance to remove auditlog.models.LogEntry entries that have passed the retention policy days')

    def execute(self):
        multi_node = True if host_count > 0 else False
        if (multi_node and not settings.API_ONLY) or not multi_node:
            to_remove = ApplicationTask.objects.filter(completed__lt=datetime.today() - timedelta(days=settings.RECORD_RETENTION))
            to_remove.delete()