from django.conf import settings
from .models import TransportLog, Message
import re

class MtaLogProcessor:
    process = None
    delay = 'delay'
    status = 'status'
    regex = r'^(\S+[0-9]\-)(\S+)\s+(\d+)\s(\d+):(\d+):(\d+)\s(\S+)\s(\S+)\[(\d+)\]:\s(.+)'
    logfile = ''

    def __init__(self, *args, **kwargs):
        self.logfile = settings.MTA_LOGFILE

    def execute(self):
        if self.process:
            current_id = None
            new_id = None
            # Read the MTA logfile
            with open(self.logfile) as f:
                for l in f.readlines():
                    # Identify the Requeueing, so that we can map the current and new queue ID
                    search = r'^.*MailScanner.*: Requeue: (\S+\.\S+) to (\S+)\s'
                    match = re.findall(search, l)
                    if match:
                        current_id = match[0]
                        new_id = match[1]
                        message = re.findall(self.regex, l)
                        if message[7] == self.process:
                            # Search the database to see if we can find an existing record and create it if necessary
                            mail = Message.objects.filter(mailq_id=current_id).get()
                            log = message[9]
                            relay_host = re.findall(r'{0}=(\S+)'.format('relay'))
                            relay_type = 'relay' if relay_host else ''
                            delay = re.findall(r'{0}=(\S+),'.format(this.delay))
                            transport_host = re.findall(r'[0-9]+\-\S+\s[0-9]+\s[0-9]+\:[0-9]+\:[0-9]+\s(\S+)')
                            dsn = re.findall(r'dsn=(\S+),')
                            dsn_message = re.findall(r'status=\S+\s\((.*)\)')
                            obj, created = TransportLog.objects.get_or_create(message=mail, relay_host=relay_host, relay_type=relay_type, delay=delay, transport_host=transport_host, dsn=dsn, dsn_message=dsn_message)

                    # Clean up
                    current_id = None
                    new_id = None

class PostfixLogProcessor(MtaLogProcessor):
    process = 'postfix/smtpd'
