from fastapi import Depends
from io import TextIOWrapper
from pathlib import Path
import logging
import re
import sys
import time
import rich
from sqlmodel import Session, select
from typing import Annotated
import typer
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from mailguardian.app.dependencies import get_database_session
from mailguardian.app.models.message import Message
from mailguardian.app.models.message_transport_log import MessageTransportIdentifier
from mailguardian.config.app import settings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
idqueue: list = []

class MilterLogFileHandler(FileSystemEventHandler):
    def __init__(self, file_path: Path | str) -> None:
        self.file_path: Path = file_path if isinstance(file_path, Path) else Path(file_path)
        self.file: TextIOWrapper = self.file_path.open('r')
        self.file.seek(0, 2) # Go to the end of the file
    def on_modified(self, event: FileSystemEvent) -> None:
        if event.src_path == str(self.file_path):
            for line in self.file:
                _process_milter_log_entry(line.strip())
            process_sql()

def _process_milter_log_entry(line: str) -> None:
    global idqueue
    # Watch for message-id's
    match = re.match(r'^.*postfix/cleanup.*: (\S+): message-id=(\S+)$', line)
    if match:
        smtpid = match.group(1)
        message_id = match.group(2)
        arr_entry = [smtpid, message_id, int(time.time()), None]
        idqueue.append(arr_entry)
        logging.debug(f'{__name__}: Added smtpid {smtpid} to relay queue')
    # Watch for verifications
    elif re.match(r'^.*postfix/smtp.*: (\S+):.*status=(?:deliverable|undeliverable)', line):
        match = re.match(r'^.*postfix/smtp.*: (\S+):.*status=(?:deliverable|undeliverable)', line)
        if match:
            smtpid = match.group(1)
            remove_entry(smtpid)
            logging.debug(f'{__name__}: Removed smtpid {smtpid} from relay queue (delivery verification)')
    # Watch for milter connections
    elif re.match(r'^.*postfix/cleanup.*: (\S+): milter', line):
        match = re.match(r'^.*postfix/cleanup.*: (\S+): milter', line)
        if match:
            smtpid = match.group(1)
            remove_entry(smtpid)
            logging.debug(f'{__name__}: Removed smtpid {smtpid} from relay queue (milter activity)')
    # Watch for delivery attempts (after verification check above)
    elif re.match(r'^.*postfix/smtp.*: (\S+): to=<(\S+)>,', line):
        match = re.match(r'^.*postfix/smtp.*: (\S+): to=<(\S+)>,', line)
        if match:
            smtpid = match.group(1)
            recipient = match.group(2)
            for entry in idqueue:
                if entry[0] == smtpid:
                    entry[3] = recipient
                    logging.debug(f'{__name__}: Delivery attempt for smtpid {smtpid} detected and updated in queue')
                    break

def process_sql(db: Annotated[Session, Depends(get_database_session)]):
    global idqueue

    idcount = len(idqueue)
    i = 0

    while i < idcount:
        if idqueue[i][3] is not None:
            message_id = idqueue[i][1]
            to = idqueue[i][3]
            smtp_id = idqueue[i][0]
            message: Message = db.exec(select(Message).where(Message.mail_message_id == message_id and Message.to_address == to)).first()
            # query = f"SELECT mailq_id FROM `messages` WHERE mail_message_id='{message_id}' AND to_address LIKE '%{to}%' LIMIT 1;"
            # result = dbquery(query)
            smtps_id = message.mailq_id

            logging.debug(f'milter_relay: idqueue {i} of {idcount - 1} / {smtp_id} / {message_id} / {to} => {smtps_id}')

            if smtps_id and smtps_id != smtp_id:
                mtalog_ids: MessageTransportIdentifier = db.exec(select(MessageTransportIdentifier).where(MessageTransportIdentifier.smtpd_id == smtps_id and MessageTransportIdentifier.smtp_id == smtp_id))
                if not mtalog_ids:
                    mtalog_ids = MessageTransportIdentifier(smtpd_id=smtps_id, smtp_id=smtp_id)
                    db.add(mtalog_ids)
                    db.commit()
                # replace_query = f"REPLACE INTO `mtalog_ids` VALUES ('{smtps_id}', '{smtp_id}')"
                # dbquery(replace_query)
                idqueue.pop(i)  # Removes the current element from the queue
                idcount -= 1
                i -= 1
                logging.debug(f'milter_relay: maillog hit for {smtp_id} entry logged and removed from queue')

        i += 1

def remove_entry(smtpid):
    global idqueue
    idqueue = [entry for entry in idqueue if entry[0] != smtpid]

    logging.debug(f'{__name__}: Removed smtpid {smtpid} from relay queue')

app: typer.Typer = typer.Typer()

@app.command(name='process')
def milter_maillog(follow: Annotated[bool, typer.Option('--follow', help='Will watch the logfile for any changes and process them')] = False, test: Annotated[bool, typer.Option('--test', help='Verify if the script is working by providing a set of sample lines')] = False):
    if test:
        print('Running simulation...')
        sample_lines: list[str] = [
            "postfix/cleanup[12345]: ABC123: message-id=<some.message.id>",
            "postfix/smtp[12345]: ABC123: to=<recipient@example.com>, relay=some.relay.com, status=deliverable",
            "postfix/cleanup[12345]: ABC123: milter",
            "postfix/smtp[12345]: ABC123: to=<another.recipient@example.com>, relay=another.relay.com, status=undeliverable"
        ]
        for line in sample_lines:
            _process_milter_log_entry(line=line.strip())
    elif follow:
        event_handler: MilterLogFileHandler = MilterLogFileHandler(file_path=settings.MTA_LOGFILE)
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
        for line in sys.stdin:
            _process_milter_log_entry(line=line.strip())