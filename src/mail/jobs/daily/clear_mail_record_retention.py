from django_extensions.management.jobs import DailyJob
from mail.models import Message
from core.models import MailScannerHost
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Job(DailyJob):
    help = _('Daily database maintenance to remove mail.models.Message entries that have passed the retention policy days')

    def execute(self):
        host_count = MailScannerHost.objects.count()
        multi_node = True if host_count > 0 else False
        if (multi_node and not settings.API_ONLY) or not multi_node:
            to_remove = Message.objects.filter(date__lt=datetime.today() - timedelta(days=settings.RECORD_RETENTION))
            # Remove files from filesystem before we delete the record in the database
            for message in to_remove:
                print('Removing {}'.format(message.mailq_id))
            #     message.remove_file()
            to_remove.delete()