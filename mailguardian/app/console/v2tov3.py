import datetime
import uuid
from dotenv import load_dotenv
import rich
from sqlmodel import Session
from typing import Any, Dict, List, Optional, Annotated
import typer
from pathlib import Path
from pydantic import PostgresDsn
import psycopg
import os
from mailguardian.app.utils.spamassassin import extract_rules_and_scores_from_report
from mailguardian.config.app import ENV_FILE as APP_ENV_FILE

app: typer.Typer = typer.Typer(help='Utilities related to switching/upgrading from 2.x.x to 3.0.0')

def __build_dict_from_cursor_tuple(cr: psycopg.Cursor, row: tuple) -> dict[str, Any]:
    """ Extract the information from the cursor on what columns/fields are fetched
        and buld a dict with each key-value-pair corresponding to a column and the value of the specific record
    """
    return {d.name: row[i] for i, d in enumerate(cr.description)}

def __build_tuple_from_dict(data: dict) -> tuple:
    """ Does the inverse of __build_dict_from_cursor_tuple where we convert a dict into a tuple that can then be used for parameters on a database cursor"""
    return tuple(data.values())

def migrate_domains(src: psycopg.Cursor, target: psycopg.Cursor) -> None:
    from mailguardian.app.schemas.domain import ReceptionType
    length: int = 0
    src.execute('SELECT count(id) FROM domains_domain')
    length = src.fetchone()[0]
    rich.print(f'[bold white]Migrating {length} domains to new database structure ...[/bold white]')
    with typer.progressbar(length=length) as progress:
        for result in src.stream("SELECT id, name, destination, relay_type, created_timestamp, updated_timestamp, active, catchall, receive_type FROM domains_domain"):
            data: dict[str, Any] = __build_dict_from_cursor_tuple(cr=src, row=result)
            data['reception_type'] = ReceptionType.FAILOVER if data['receive_type'] == 'failover' else ReceptionType.LOAD_BALANCED
            data.pop('receive_type')
            target.execute('INSERT INTO domains (uuid, name, destination, relay_type, created_at, updated_at, active, catchall, reception_type) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id', __build_tuple_from_dict(data))
            progress.update(1)
    print(f'Processed {length} domains')

def migrate_users(src: psycopg.Cursor, target: psycopg.Cursor) -> None:
    from mailguardian.app.schemas.user import UserRole
    length: int = 0
    src.execute('SELECT count(id) from core_user WHERE email <> %s', ['AnonymousUser'])
    length = src.fetchone()[0]
    rich.print(f'[bold white]Migrating {length} users to new database structure ...[/bold white]')
    with typer.progressbar(length=length) as progress:
        for result in src.stream("SELECT id, first_name, last_name, email, password, is_staff, is_domain_admin, is_active, date_joined, last_login, daily_quarantine_report, weekly_quarantine_report, monthly_quarantine_report, custom_spam_score, custom_spam_highscore, skip_scan FROM core_user WHERE email <> %s", ['AnonymousUser']):
            data: dict[str, Any] = __build_dict_from_cursor_tuple(cr=src, row=result)
            if data['is_staff']:
                data['role'] = UserRole.SUPERUSER
            elif data['is_domain_admin']:
                data['role'] = UserRole.DOMAIN_ADMINISTRATOR
            else:
                data['role'] = UserRole.USER
            data.pop('is_staff')
            data.pop('is_domain_admin')
            # NOTE: The new User model is not yet fully built, so we construct a new dict with just the information that we need and then we will fill in the rest later
            new_data: dict[str, Any] = {
                'uuid': data['id'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'password': data['password'].replace('argon2$', '$'), # This makes the hashes from Django, compatible with passlib
                'role': data['role'],
                'is_active': data['is_active'],
                'created_at': data['date_joined']
            }
            target.execute('INSERT INTO users (uuid, first_name, last_name, email, password, role, is_active, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id', __build_tuple_from_dict(new_data))
            progress.update(1)
    print(f'Processed {length} users')

def migrate_messages(src: psycopg.Cursor, target: psycopg.Cursor) -> None:
    length: int = 0
    src.execute('SELECT count(id) FROM mail_message')
    length = src.fetchone()[0]
    query: str = str(("SELECT mm.id, "
            "mm.from_address, "
            "mm.from_domain, "
            "mm.to_address, "
            "mm.to_domain, "
            "mm.subject, "
            "mm.client_ip, "
            "mm.mailscanner_hostname, "
            "mm.spam_score, "
            "mm.mcp_score, "
            "mm.timestamp, "
            "mm.date, "
            "mm.size, "
            "mm.token, "
            "mm.mailq_id, "
            "mm.is_spam, "
            "mm.is_mcp, "
            "mm.is_rbl_listed, "
            "mm.infected, "
            "mm.stored, "
            "mm.scanned, "
            "mm.allowed, "
            "mm.blocked,"
            "mh.contents AS headers,"
            "mmsr.contents AS mailscanner_report,"
            "mcp.contents AS mcp_report,"
            "rbl.contents AS rbl_report,"
            "msr.contents AS spam_report "
        "FROM mail_message AS mm "
        "LEFT JOIN mail_headers AS mh ON mh.message_id = mm.id "
        "LEFT JOIN mail_mailscannerreport AS mmsr ON mmsr.message_id = mm.id "
        "LEFT JOIN mail_mcpreport AS mcp ON mcp.message_id = mm.id "
        "LEFT JOIN mail_rblreport AS rbl ON rbl.message_id = mm.id "
        "LEFT JOIN mail_spamreport AS msr ON msr.message_id = mm.id"))
    
    rich.print(f'[bold white]Migrating {length} messages to new database structure ...[/bold white]')

    with typer.progressbar(length=length) as progress:
        for result in src.stream(query=query):
            data: dict[str, Any] = __build_dict_from_cursor_tuple(cr=src, row=result)
            headers: str = data.pop('headers', '')
            mailscanner_report: str = data.pop('mailscanner_report', '')
            mcp_report: str = data.pop('mcp_report', '')
            rbl_report: str = data.pop('rbl_report', '')
            spam_report: str = data.pop('spam_report', '')
            data['spam_score'] = data['spam_score'] or 0.00
            data['mcp_score'] = data['mcp_score'] or 0.00
            data['timestamp'] = data['timestamp'] + datetime.timedelta(days=(365*7) - 10)
            data['date'] = data['date'] + datetime.timedelta(days=(365*7) - 10)
            target.execute(("INSERT INTO messages "
                "("
                    "uuid, "
                    "from_address, "
                    "from_domain, "
                    "to_address, "
                    "to_domain, "
                    "subject, "
                    "client_ip, "
                    "mailscanner_hostname, "
                    "spam_score, "
                    "mcp_score, "
                    "timestamp, "
                    "date, "
                    "size, "
                    "token, "
                    "mailq_id, "
                    "is_spam, "
                    "is_mcp, "
                    "is_rbl_listed, "
                    "infected, "
                    "stored, "
                    "scanned, "
                    "allowed, "
                    "blocked"
                ")" 
                "VALUES("
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s, "
                    "%s"
                ") RETURNING id"), __build_tuple_from_dict(data=data))
            
            record_id = target.fetchone()[0]
            if headers:
                raw: List[str] = headers.replace('\r\n\t', '').splitlines()
                previous: str = ''
                to_insert: Dict[str, str] = {}
                for h in raw:
                    data = h.split(': ', 1)
                    if len(data) > 1:
                        to_insert[data[0]] = data[1].replace('\r\n ', '\r\n')
                        previous = data[0]
                    else:
                        to_insert[previous] += '\r\n' + data[0].replace(' ', '')
                for header in to_insert.keys():
                    # print(headers)
                    # TODO: Create one big query with all headers
                    q: str = 'INSERT INTO message_headers (message_id, uuid, key, value) VALUES'
                    vals = [
                        record_id,
                        str(uuid.uuid4()),
                        header,
                        to_insert[header]
                    ]
                    args = target
                    target.execute('INSERT INTO message_headers (message_id, uuid, key, value) VALUES(%s, %s, %s, %s)', [
                        record_id,
                        str(uuid.uuid4()),
                        header,
                        to_insert[header]
                    ])
            # if mailscanner_report:
            #     target.execute('INSERT INTO message_mailscanner_reports (message_id, uuid, contents) VALUES(%s, %s, %s)', [
            #         record_id,
            #         str(uuid.uuid4()),
            #         mailscanner_report
            #     ])
            if mcp_report:
                target.execute('INSERT INTO message_mcp_reports (message_id, uuid, contents) VALUES(%s, %s, %s)', [
                    record_id,
                    str(uuid.uuid4()),
                    mcp_report
                ])
            if rbl_report:
                target.execute('INSERT INTO message_rbl_reports (message_id, uuid, contents) VALUES(%s, %s, %s)', [
                    record_id,
                    str(uuid.uuid4()),
                    rbl_report
                ])
            if spam_report:
                vals: list[dict[str, float]] = extract_rules_and_scores_from_report(spamreport=spam_report)
                for val in vals:
                    values: list = [record_id, uuid.uuid4(), val.get('rule'), val.get('score')]
                    if val.get('rule') == 'too' and val.get('score') == 'large':
                        values = [record_id, uuid.uuid4(), f'{val.get("rule")} {val.get("score")}', 0.0]
                    target.execute('INSERT INTO message_spam_reports (message_id, uuid, rule, score) VALUES(%s, %s, %s, %s)', values)
                # raw = spam_report.replace('not spam, ', '').replace('not spam (too large)', 'too large').replace('spam( ', '').replace('spam, ', '').replace('SpamAssassin (', '').replace('not cached, ', '').replace(')', '').replace('autolearn=', '').split(', ')
                # if 'too large' in raw:
                #     vals.append([
                #         record_id,
                #         str(uuid.uuid4()),
                #         'TOO_LARGE',
                #         0.0
                #     ])
                # else:
                #     raw.pop()
                # for entry in raw:
                #     if entry == 'too large':
                #         continue
                #     if not entry.startswith('required'):
                #         try:
                #             key, value = entry.split(' ')
                #             vals.append([
                #                 record_id,
                #                 str(uuid.uuid4()),
                #                 key,
                #                 value
                #             ])
                #         except:
                #             pass
                # for val in vals:
                #     target.execute('INSERT INTO message_spam_reports (message_id, uuid, rule, score) VALUES(%s,%s,%s, %s)', val)
            progress.update(1)
    print(f'Processed {length} messages')

def migrate_list_entries(src: psycopg.Cursor, target: psycopg.Cursor) -> None:
    from mailguardian.app.schemas.list_entry import ListingType
    length: int = 0
    src.execute('SELECT count(id) FROM domains_domain')
    length = src.fetchone()[0]
    rich.print(f'[bold white]Migrating {length} entries of allowed senders and blocked senders to new database structure ...[/bold white]')
    with typer.progressbar(length=length) as progress:
        for result in src.stream('SELECT id, from_address, from_domain, to_address, to_domain, listing_type FROM list_entries'):
            data: dict[str, Any] = __build_dict_from_cursor_tuple(cr=src, row=result)
            data['listing_type'] = str(data['listing_type']).upper()
            target.execute('INSERT INTO list_entries (uuid, from_address, from_domain, to_address, to_domain, listing_type) VALUES(%s, %s, %s, %s, %s, %s)', __build_tuple_from_dict(data))
            progress.update(1)
    print(f'Processed {length} entries of allowed senders and blocked senders')


@app.command(name='migrate', help='Migrate data from MailGuardian 2.x.x to MailGuardian 3.0.0')
def migrate_v2tov3(
        env_file: Path = Path(APP_ENV_FILE.parent, '.env.migrate'), 
        all: Annotated[bool, typer.Option('--all', help='Migrate all compatible records')] = False, 
        messages: Annotated[bool, typer.Option('--messages', help='Migrate processed messages and their metadata')] = False, 
        domains: Annotated[bool, typer.Option('--domains', help='Migrate the domains being handled')] = False, 
        compliance: Annotated[bool, typer.Option('--compliance', help='Migrate compatible data related to GDPR compliance and audit')] = False, 
        users: Annotated[bool, typer.Option('--users', help='Migrated users of the application')] = False,
        lists: Annotated[bool, typer.Option('--lists', help='Migrated allowed/blocked senders')] = False,
        hosts: Annotated[bool, typer.Option('--hosts', help='Migrate configuration data for hosts that process data')] = False,
        relays: Annotated[bool, typer.Option('--relays', help='Migrate configuration related to hosts sending email')] = False,
        spamassassin: Annotated[bool, typer.Option('--sa-rules', help='Migrate custom SpamAssassin rules and descriptions')] = False,
    ):
    load_dotenv(env_file)
    source_dsn: str = PostgresDsn.build(
        scheme="postgresql",
        username=os.environ.get("SOURCE_POSTGRES_USER"),
        password=os.environ.get("SOURCE_POSTGRES_PASSWORD"),
        host=os.environ.get("SOURCE_POSTGRES_SERVER"),
        port=int(os.environ.get("SOURCE_POSTGRES_PORT", 5432)),
        path=f"{os.environ.get('SOURCE_POSTGRES_DB') or ''}",
    ).unicode_string()
    target_dsn: str = PostgresDsn.build(
        scheme="postgresql",
        username=os.environ.get("TARGET_POSTGRES_USER"),
        password=os.environ.get("TARGET_POSTGRES_PASSWORD"),
        host=os.environ.get("TARGET_POSTGRES_SERVER"),
        port=int(os.environ.get("TARGET_POSTGRES_PORT", 5432)),
        path=f"{os.environ.get('TARGET_POSTGRES_DB') or ''}",
    ).unicode_string()
    source_connection = psycopg.connect(source_dsn, autocommit=False)
    rich.print('[bold green]Connected to source database[/bold green]')
    target_connection = psycopg.connect(target_dsn, autocommit=False)
    rich.print('[bold green]Connected to target database[/bold green]')
    src: psycopg.Cursor = source_connection.cursor()
    target: psycopg.Cursor = target_connection.cursor()

    if all:
        messages = True
        domains = True
        compliance = True
        users = True
        lists = True
        hosts = True
        relays = True
        spamassassin = True

    # Migrate messages + metadata
    if messages:
        migrate_messages(src=src, target=target)
        target_connection.commit()
    # Migrate domains
    if domains:
        migrate_domains(src=src, target=target)
        target_connection.commit()
    # Migrate App users
    if users:
        migrate_users(src=src, target=target)
    # Migrate MailGuardian hosts
    # Migrate App settings - if applicable
    # Migrate App notifications (persistent notifications for login screen and dashboard)
    # Migrate compliance logs
    # Migrate allowed senders + blocked senders
    if lists:
        migrate_list_entries(src=src, target=target)
        target_connection.commit()

    # Migrate SMTP relay settings
    # Migrate SpamAssassin rules + descriptors
