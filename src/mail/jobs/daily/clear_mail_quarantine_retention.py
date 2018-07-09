from django_extensions.management.jobs import DailyJob
from mail.models import Message
from datetime import datetime, timedelta
from django.conf import settings

class Job(DailyJob):
    help = 'Daily database maintenance to remove mail.models.Message entries that have passed the retention policy days for quarantined messages'

    def execute(self):
        to_remove = Message.objects.filter(date__lt=datetime.today() - timedelta(days=settings.QUARANTINE_RETENTION)).filter(quarantined=True)
        # Remove files from filesystem before we delete the record in the database
        for message in to_remove:
            message.remove_file()
        to_remove.delete()