from django.core.management.base import BaseCommand, CommandError
from mail.log_processors import PostfixLogProcessor

class Command(BaseCommand):
    help = 'Manually trigger a sync of the MTA transport logfile to the database'

    def handle(self, *args, **kwargs):
        mta_log_processor = PostfixLogProcessor()
        mta_log_processor.execute()