from django.conf import settings
from .models import TransportLog, Message
import re
import datetime

class MtaLogProcessor:
    process = None
    delay = r'delay=(\d+\.\d+)'
    status = r'status=(\S+)'
    logfile = ''

    def __init__(self, *args, **kwargs):
        self.logfile = settings.MTA_LOGFILE

    def execute(self):
        if self.process:
            matches = {}
            current_id = None
            new_id = None
            # Read the MTA logfile
            with open(self.logfile) as f:
                for l in f.readlines():
                    # Identify the Requeueing, so that we can map the current and new queue ID
                    search = r'^.*MailScanner.*: Requeue: (\S+\.\S+) to (\S+)\s'
                    match = re.findall(search, l)
                    if match:
                        matches[match[0][1]] = match[0][0]
                    mta_match = re.findall(self.process, l)
                    if mta_match:
                        queue_id = mta_match[0][2]
                        print(queue_id)
                        relay_host = re.findall(r"\[(\d+\.\d+\.\d+\.\d+)\]", l)
                        print(relay_host)
                        delay = re.findall(self.delay, l)
                        print(delay)
                        dsn = re.findall(r'dsn=(\d+\.\d+\.\d+)', l)
                        print(dsn)
                        status = re.findall(self.status, l)
                        print(status)
                        dsn_message = re.findall(r'\((.+)\)', l)
                        print(dsn_message)
                        timestamp_match = re.findall(r'^(\S+)\s(\d+)\s(\d+\:\d+\:\d+)', l)
                        print(timestamp_match)
                        try:
                            message = Message.objects.filter(mailq_id=matches[queue_id]).first()
                            timestamp = datetime.datetime.strptime('{0} {1} {2} {3}'.format(timestamp_match[0][0], timestamp_match[0][1], message.timestamp.year, timestamp_match[0][2]), '%b %d %Y %H:%M:%S')
                            obj, created = TransportLog.objects.update_or_create(message=message, timestamp=str(timestamp), relay_host=relay_host[0], delay=delay[0], transport_host=settings.APP_HOSTNAME, dsn=dsn[0], dsn_message=dsn_message[0])
                        except Exception as e:
                            print(e)
                    # Clean up
                    current_id = None
                    new_id = None

class PostfixLogProcessor(MtaLogProcessor):
    process = r"(postfix/smtp)(\[\d+\])\:\s(\w+)"
