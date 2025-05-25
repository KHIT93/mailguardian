from abc import ABC, abstractmethod
import datetime
from io import TextIOWrapper
import os
from pathlib import Path
import logging
import re
import sys
import time
import rich
from typing import Annotated
import typer
from fastapi import Depends
from sqlmodel import Session, select
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from mailguardian.app.models.message import Message
from mailguardian.app.models.message_transport_log import MessageTransportLog
from mailguardian.app.dependencies import get_database_session
from mailguardian.config.app import settings

# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

class SyslogParser:
    def __init__(self, line):
        # Define the months mapping
        self.months = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12,
        }

        # Parse the date, time, host, process pid and log entry
        match = re.match(r'^(\S+)\s+(\d+)\s(\d+):(\d+):(\d+)\s(\S+)\s(\S+)\[(\d+)\]:\s(.+)$', line)
        if match:
            # Store raw line
            self.raw = match.group(0)

            # Decode the syslog time/date
            month_str = match.group(1)
            day = int(match.group(2))
            hour = int(match.group(3))
            minute = int(match.group(4))
            second = int(match.group(5))
            host = match.group(6)
            process = match.group(7)
            pid = match.group(8)
            entry = match.group(9)

            month = self.months[month_str]
            this_month = datetime.now().month
            this_year = datetime.now().year

            # Determine the correct year
            year = this_year if month <= this_month else this_year - 1

            # Format date and time
            date_str = f"{year}-{month:02}-{day:02}"
            time_str = f"{hour:02}:{minute:02}:{second:02}"
            datetime_str = f"{date_str} {time_str}"

            # Parse to timestamp and RFC3339 datetime
            self.timestamp = int(time.mktime(time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')))
            self.rfctime = datetime.fromtimestamp(self.timestamp).isoformat()

            self.date = date_str
            self.time = time_str
            self.host = host
            self.process = process
            self.pid = pid
            self.entry = entry

class MtaLogProcessor(ABC):
    def __init__(self, db: Annotated[Session, Depends(get_database_session)]):
        self.mtaprocess = None
        self.delay_field = None
        self.status_field = None

        self.raw = None
        self.id = None
        self.entry = None
        self.entries = {}

        self.db = db

    @abstractmethod
    def extract_key_value_pairs(self, match):
        pass

    def get_reject_reasons(self):
        return {}

    def get_rulesets(self):
        return {}

    def process_line(self, line):
        parser = SyslogParser(line)
        _timestamp = parser.timestamp
        _host = parser.host
        _dsn = ''
        _delay = ''
        _relay = ''
        _msg_id = ''
        _status = ''
        _type = None
        _to = ''

        if parser.process == self.mtaprocess:
            self.parse(parser.entry)

            print(self.__dict__)

            _msg_id = self.id

            # Apply rulesets if they exist
            rulesets = self.get_rulesets()
            _type = rulesets.get('type', _type)
            _relay = rulesets.get('relay', _relay)
            _status = rulesets.get('status', _status)

            # Milter-ahead rejections
            if 'Milter: ' in self.raw and re.search(r'(rejected recipient|user unknown)', self.entries.get('reject', '')):
                _type = 'unknown_user'
                _status = self.get_email()

            # Unknown users
            if re.search(r'user unknown', self.entry, re.IGNORECASE):
                _type = 'unknown_user'
                _status = self.raw

            # Apply reject reasons if they exist
            reject_reasons = self.get_reject_reasons()
            _type = reject_reasons.get('type', _type)
            _status = reject_reasons.get('status', _status)

            # Relay lines
            if 'relay' in self.entries and self.status_field in self.entries:
                _to = self.entries.get('to')
                _type = 'relay'
                _delay = self.entries.get(self.delay_field)
                _relay = self.get_ip()
                _dsn = self.entries.get('dsn')
                _status = self.entries.get(self.status_field)

        if _type is not None:
            if re.match(r'^\d+$', _delay):
                message: Message = self.db.exec(select(Message).where(Message.mailq_id == _msg_id)).first()
                log_entry = MessageTransportLog(timestamp=_timestamp, transport_host=_host, relay_host=_relay, transport_type=_type, dsn=_dsn, dsn_message=_status, delay=_delay, message=message or None)
                self.db.add(log_entry)
                self.db.commit()
            else:
                message: Message = self.db.exec(select(Message).where(Message.mailq_id == _msg_id)).first()
                log_entry = MessageTransportLog(timestamp=_timestamp, transport_host=_host, relay_host=_relay, transport_type=_type, dsn=_dsn, dsn_message=_status, delay=_delay, message=message or None)
                self.db.add(log_entry)
                self.db.commit()

    def follow(self, file):
        size = os.path.getsize(file)
        lines = 1

        while True:
            current_size = os.path.getsize(file)
            if size == current_size:
                time.sleep(1)
                continue

            with open(file, 'rb') as fh:
                fh.seek(size)

                for line in fh:
                    self.process_line(line.decode('utf-8'))
                    lines += 1

            size = current_size

    def doit(self, input_cmd):
        try:
            fp = os.popen(input_cmd)
            lines = 1
            for line in fp:
                self.process_line(line)
                lines += 1
            fp.close()
        except Exception as e:
            sys.exit(f"Error: {e}")

    def parse(self, line):
        self.id = None
        self.entry = None
        self.entries = {}
        self.raw = line

        match = re.match(r'^(\S+):\s(.+)$', line)
        if match:
            self.id = match.group(1)

            milter_match = re.match(r'(\S+):\sMilter:\s(.+)$', line)
            if milter_match:
                match = milter_match

            # Extract key-value pairs
            if '=' in match.group(2):
                self.entries = self.extract_key_value_pairs(match)
            else:
                self.entry = match.group(2)
            return True

        # No message ID found; extract key-value pairs directly
        if '=' in self.raw:
            items = self.raw.split(', ')
            entries = {}
            for item in items:
                entry = item.split('=')
                if len(entry) > 2:
                    entries[entry[0]] = '='.join(entry[1:])
                elif len(entry) == 2:
                    entries[entry[0]] = entry[1]
            self.entries = entries
            return True

        return False

    def get_ip(self):
        match = re.search(r'\[(\d+\.\d+\.\d+\.\d+)\]', self.entries.get('relay', ''))
        return match.group(1) if match else self.entries.get('relay', '')

    def get_email(self):
        match = re.search(r'<(\S+)>', self.entries.get('to', ''))
        return match.group(1) if match else self.entries.get('to', '')

class PostfixLogProcessor(MtaLogProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.mtaprocess = 'postfix/smtp'
        self.delay_field = 'delay'
        self.status_field = 'status'

    def get_reject_reasons(self):
        reject_reasons = {}
        if 'NOQUEUE' in self.entry.upper():
            if re.search(r'Client host rejected: cannot find your hostname', self.entry, re.IGNORECASE):
                reject_reasons['type'] = 'unknown_hostname'
            else:
                reject_reasons['type'] = 'NOQUEUE'
            reject_reasons['status'] = self.raw
        return reject_reasons

    def extract_key_value_pairs(self, match):
        pattern = (
            r"to=<(?P<to>[^>]*)>, "
            r"(?:orig_to=<(?P<orig_to>[^>]*)>, )?"
            r"relay=(?P<relay>[^,]+), "
            r"(?:conn_use=(?P<conn_use>[^,]+), )?"
            r"delay=(?P<delay>[^,]+), "
            r"(?:delays=(?P<delays>[^,]+), )?"
            r"(?:dsn=(?P<dsn>[^,]+), )?"
            r"status=(?P<status>.*)$"
        )
        entries = re.match(pattern, match.group(2))
        return entries.groupdict() if entries else {}
    
class PostfixLogFileHandler(FileSystemEventHandler):
    def __init__(self, file_path: Path | str, log_processor: MtaLogProcessor) -> None:
        self.file_path: Path = file_path if isinstance(file_path, Path) else Path(file_path)
        self.file: TextIOWrapper = self.file_path.open('r')
        self.log_processor: MtaLogProcessor = log_processor
        self.file.seek(0, 2) # Go to the end of the file
    def on_modified(self, event: FileSystemEvent) -> None:
        if event.src_path == str(self.file_path):
            for line in self.file:
                self.log_processor.process_line(line.strip())

app: typer.Typer = typer.Typer()

@app.command(name='process')
def postfix_maillog(follow: Annotated[bool, typer.Option('--follow', help='Will watch the logfile for any changes and process them')] = False, test: Annotated[bool, typer.Option('--test', help='Verify if the script is working by providing a set of sample lines')] = False):
    log_processor: PostfixLogProcessor = PostfixLogProcessor()
    if test:
        print('Running simulation...')
        pass
    elif follow:
        event_handler: PostfixLogFileHandler = PostfixLogFileHandler(file_path=settings.MTA_LOGFILE)
        observer = Observer()
        observer.schedule(event_handler=event_handler, path=settings.MTA_LOGFILE, recursive=False)
        observer.start()
        try:
            print(f'Watching Logfile: {settings.MTA_LOGFILE}')
            while True:
                observer.join(1)
        except KeyboardInterrupt:
            observer.stop()
        
        observer.join()
    elif not follow:
        print('Processing stdin...')
        for line in sys.stdin:
            log_processor.process_line(line.strip())