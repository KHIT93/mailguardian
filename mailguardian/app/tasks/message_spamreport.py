from fastapi import Depends
from sqlmodel import Session
from typing import Annotated, Any
from mailguardian.app.dependencies import get_database_session
from mailguardian.app.models.message_spam_report import MessageSpamReport
from mailguardian.app.utils.spamassassin import extract_rules_and_scores_from_report

def spamassassin_report_to_db(db: Annotated[Session, Depends(get_database_session)], payload: dict[str, Any]):
    formatted_report: list[dict[str, str]] = extract_rules_and_scores_from_report(spamreport=payload.get('spamreport'))
    message_id: int = payload.get('message_id')
    db.add_all([MessageSpamReport(**entry, message_id=message_id) for entry in formatted_report])
    db.commit()

    