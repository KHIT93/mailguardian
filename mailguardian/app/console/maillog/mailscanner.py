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

# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
idqueue: list = []

class MilterLogFileHandler(FileSystemEventHandler):
    def __init__(self, file_path: Path | str) -> None:
        self.file_path: Path = file_path if isinstance(file_path, Path) else Path(file_path)
        self.file: TextIOWrapper = self.file_path.open('r')
        self.file.seek(0, 2) # Go to the end of the file
    def on_modified(self, event: FileSystemEvent) -> None:
        if event.src_path == str(self.file_path):
            for line in self.file:
                _process_mailscanner_log_entry(line=line.strip())

def _process_mailscanner_log_entry(db: Annotated[Session, Depends(get_database_session)], line: str) -> None:
    match = re.match(r'^.*MailScanner.*: Requeue: (\S+\.\S+) to (\S+)\s$', line)
    if match:
        smtpd_id = match.group(1)
        smtp_id = match.group(2)
        mtalog_ids: MessageTransportIdentifier = db.exec(select(MessageTransportIdentifier).where(MessageTransportIdentifier.smtpd_id == smtpd_id and MessageTransportIdentifier.smtp_id == smtp_id))
        if not mtalog_ids:
            mtalog_ids = MessageTransportIdentifier(smtpd_id=smtpd_id, smtp_id=smtp_id)
            db.add(mtalog_ids)
            db.commit()

app: typer.Typer = typer.Typer()

@app.command(name='process')
def mailscanner_maillog(follow: Annotated[bool, typer.Option('--follow', help='Will watch the logfile for any changes and process them')] = False, test: Annotated[bool, typer.Option('--test', help='Verify if the script is working by providing a set of sample lines')] = False):
    if follow:
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
            _process_mailscanner_log_entry(line=line.strip())