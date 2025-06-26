import re
from typing import Annotated

from sqlmodel import Session, select

from mailguardian.app.models.spamassassin_rule_description import (
    SpamAssassinRuleDescription,
)
from mailguardian.app.service_providers.dependency_injection import (
    Depends,
    inject_dependencies,
)
from mailguardian.database.connect import Database

# List of non-rule lines
not_rules_lines: list[str] = [
    'cached', 'score=', 'required', 'autolearn=',
    'punteggio=', 'necessario',
    'benoetigt', 'Wertung=', 'gecached',
    'requis'
]
# Remove 'score=', 'required', and similar lines
not_rules_lines_regex: str = '|'.join(map(re.escape, not_rules_lines))


@inject_dependencies()
def get_sa_rule_desc(db_connection: Annotated[Database, Depends()], rule: str) -> dict[str, str] | bool:
    db: Session = db_connection.get_session()
    # Initialize rule score
    rule_score = ''

    # Split the rule into its components
    match = re.match(r'^(.+) (.+)$', rule)
    if match:
        rule = match.group(1)
        rule_score = match.group(2)  # noqa: F841

    record: SpamAssassinRuleDescription = db.exec(select(SpamAssassinRuleDescription).where(SpamAssassinRuleDescription.key == rule)).first()
    if record:
        return {
            rule: record.value
        }

    else:
        return False


@inject_dependencies()
def format_spamassassin_report(db_connection: Annotated[Database, Depends()], spamreport: str) -> list[dict[str, str]] | str:
    # Run regex against the MailScanner spamreport picking out the (score=xx, required x, RULES...)
    match = re.search(r'\s\((.+?)\)', spamreport, re.IGNORECASE)  # noqa: F841

    with db_connection.session_scope() as db:
        sa_rules: list[dict[str, float]] = extract_rules_and_scores_from_report(spamreport=spamreport)

        # Get rule descriptions
        output_array: list[dict[str, str]] = [get_sa_rule_desc(db=db, rule=f"{sa_rule.get('rule')} {sa_rule.get('score')}") for sa_rule in sa_rules]

        if output_array and any(a for a in output_array):
            return output_array
        else:
            return spamreport


def extract_rules_and_scores_from_report(spamreport: str) -> list[dict[str, float]]:
    # Run regex against the MailScanner spamreport picking out the (score=xx, required x, RULES...)
    match = re.search(r'\s\((.+?)\)', spamreport, re.IGNORECASE)

    if match:
        # Extract and split the matched group
        sa_rules = match.group(1).split(', ')

        # Check if a valid check was run
        if sa_rules[0] in ['Message larger than max testing size', 'timed out']:
            return sa_rules[0]

        # Remove 'score=', 'required', and similar lines
        sa_rules: list[dict[str, float]] = [{'rule': rule.split(' ')[0], 'score': rule.split(' ')[1]} for rule in sa_rules if not re.search(not_rules_lines_regex, rule, re.IGNORECASE)]

        if sa_rules:
            return sa_rules
        else:
            return spamreport
    # Regular expression did not match, return unmodified report instead
    else:
        return spamreport
