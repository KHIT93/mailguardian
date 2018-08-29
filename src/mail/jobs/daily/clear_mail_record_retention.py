from django_extensions.management.jobs import DailyJob
from mail.models import Message
from datetime import datetime, timedelta
from django.conf import settings

class Job(DailyJob):
    help = 'Daily database maintenance to remove mail.models.Message entries that have passed the retention policy days'

    def execute(self):
        multi_node = True if host_count > 0 else False
        if (multi_node and not settings.API_ONLY) or not multi_node:
            to_remove = Message.objects.filter(date__lt=datetime.today() - timedelta(days=settings.RECORD_RETENTION))
            # Remove files from filesystem before we delete the record in the database
            for message in to_remove:
                message.remove_file()
            to_remove.delete()