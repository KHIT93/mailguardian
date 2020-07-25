from django.core.management.base import BaseCommand, CommandError
from mail.log_processors import PostfixLogProcessor
from django.conf import settings
import os
from django.utils.translation import gettext_lazy as _

class Command(BaseCommand):
    help = _('Manually trigger a sync of the MTA transport logfile to the database')

    def handle(self, *args, **kwargs):
        if not os.access(settings.MTA_LOGFILE, os.R_OK):
            print(_('You are not authorized to read the file %(file)s. Please verify that you have the correct permissions or that you are running this command as root' % settings.MTA_LOGFILE))
        else:
            mta_log_processor = PostfixLogProcessor()
            mta_log_processor.execute()