from fastapi import Depends
from injector import inject
from sqlmodel import Session
from typing import Annotated, Any
from mailguardian.app import services
from mailguardian.app.dependencies import get_database_session
from mailguardian.app.models.message_spam_report import MessageSpamReport
from mailguardian.app.utils.spamassassin import extract_rules_and_scores_from_report
from mailguardian.database.connect import Database

def spamassassin_report_to_db(payload: dict[str, Any]):
    db: Session = services.get(Database).get_session()
    formatted_report: list[dict[str, str]] = extract_rules_and_scores_from_report(spamreport=payload.get('spamreport'))
    message_id: int = payload.get('message_id')
    db.add_all([MessageSpamReport(**entry, message_id=message_id) for entry in formatted_report])
    db.commit()

    