import re
from sqlmodel import Session
from typing import Annotated, Any
from mailguardian.app.models.message_header import MessageHeader
from mailguardian.app.service_providers.dependency_injection import Depends, inject_dependencies
from mailguardian.database.connect import Database

@inject_dependencies()
def message_headers_to_db(db_connection: Annotated[Database, Depends()], payload: dict[str, Any]):
    db: Session = db_connection.get_session()
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

    