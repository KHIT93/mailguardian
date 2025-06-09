from fastapi import Depends
import re
from injector import inject
from sqlmodel import Session
from typing import Annotated, Any
from mailguardian.app import services
from mailguardian.app.dependencies import get_database_session
from mailguardian.app.models.message_header import MessageHeader
from mailguardian.database.connect import Database

def message_headers_to_db(payload: dict[str, Any]):
    db: Session = services.get(Database).get_session()
    message_id: int = payload.get('message_id')
    headers: dict[str, Any] = {}
    lines: list[str] = payload.get('headers').splitlines()
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue
        
        # Check if the line starts with whitespace (indicating a continuation of the previous line)
        if line.startswith(' ') and headers:
            # Append to the last header's value
            last_key = list(headers.keys())[-1]
            headers[last_key] += " " + line.strip()
        else:
            # Split the line into key and value at the first colon
            match = re.match(r'^([^:]+):\s*(.*)$', line)
            if match:
                key, value = match.groups()
                headers[key] = value.strip()
    db.add_all([MessageHeader(message_id=message_id, key=header, value=headers[header]) for header in headers.keys()])
    db.commit()

    