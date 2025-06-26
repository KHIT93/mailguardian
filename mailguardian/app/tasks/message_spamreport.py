from typing import Annotated, Any

from sqlmodel import Session

from mailguardian.app.models.message_spam_report import MessageSpamReport
from mailguardian.app.service_providers.dependency_injection import (
    Depends,
    inject_dependencies,
)
from mailguardian.app.utils.spamassassin import extract_rules_and_scores_from_report
from mailguardian.database.connect import Database


@inject_dependencies()
def spamassassin_report_to_db(db_connection: Annotated[Database, Depends()], payload: dict[str, Any]):
    db: Session = db_connection.get_session()
    formatted_report: list[dict[str, str]] = extract_rules_and_scores_from_report(spamreport=payload.get('spamreport'))
    message_id: int = payload.get('message_id')
    db.add_all([MessageSpamReport(**entry, message_id=message_id) for entry in formatted_report])
    db.commit()
