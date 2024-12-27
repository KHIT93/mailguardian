"""empty message

Revision ID: 5484b266d10b
Revises: 
Create Date: 2024-04-24 22:25:09.283948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = '5484b266d10b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('domains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('destination', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('relay_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('catchall', sa.Boolean(), nullable=False),
    sa.Column('reception_type', sa.Enum('LOAD_BALANCED', 'FAILOVER', name='receptiontype'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_domains_name'), 'domains', ['name'], unique=True)
    op.create_index(op.f('ix_domains_uuid'), 'domains', ['uuid'], unique=False)
    op.create_table('list_entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('from_address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('from_domain', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('to_address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('to_domain', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('listing_type', sa.Enum('ALLOWED', 'BLOCKED', name='listingtype'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_list_entries_from_address'), 'list_entries', ['from_address'], unique=False)
    op.create_index(op.f('ix_list_entries_from_domain'), 'list_entries', ['from_domain'], unique=False)
    op.create_index(op.f('ix_list_entries_listing_type'), 'list_entries', ['listing_type'], unique=False)
    op.create_index(op.f('ix_list_entries_to_address'), 'list_entries', ['to_address'], unique=False)
    op.create_index(op.f('ix_list_entries_to_domain'), 'list_entries', ['to_domain'], unique=False)
    op.create_index(op.f('ix_list_entries_uuid'), 'list_entries', ['uuid'], unique=False)
    op.create_table('mailscanner_hosts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('hostname', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('ip_address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('use_tls', sa.Boolean(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.Column('passive', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mailscanner_hosts_ip_address'), 'mailscanner_hosts', ['ip_address'], unique=False)
    op.create_index(op.f('ix_mailscanner_hosts_uuid'), 'mailscanner_hosts', ['uuid'], unique=False)
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('from_address', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('from_domain', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('to_address', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('to_domain', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('subject', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('client_ip', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('mailscanner_hostname', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('spam_score', sa.Float(), nullable=False),
    sa.Column('mcp_score', sa.Float(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('size', sa.Float(), nullable=False),
    sa.Column('token', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('mailq_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('allowed', sa.Boolean(), nullable=False),
    sa.Column('blocked', sa.Boolean(), nullable=False),
    sa.Column('is_spam', sa.Boolean(), nullable=False),
    sa.Column('is_mcp', sa.Boolean(), nullable=False),
    sa.Column('is_rbl_listed', sa.Boolean(), nullable=False),
    sa.Column('stored', sa.Boolean(), nullable=False),
    sa.Column('infected', sa.Boolean(), nullable=False),
    sa.Column('scanned', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_allowed'), 'messages', ['allowed'], unique=False)
    op.create_index(op.f('ix_messages_blocked'), 'messages', ['blocked'], unique=False)
    op.create_index(op.f('ix_messages_client_ip'), 'messages', ['client_ip'], unique=False)
    op.create_index(op.f('ix_messages_date'), 'messages', ['date'], unique=False)
    op.create_index(op.f('ix_messages_from_address'), 'messages', ['from_address'], unique=False)
    op.create_index(op.f('ix_messages_from_domain'), 'messages', ['from_domain'], unique=False)
    op.create_index(op.f('ix_messages_infected'), 'messages', ['infected'], unique=False)
    op.create_index(op.f('ix_messages_is_mcp'), 'messages', ['is_mcp'], unique=False)
    op.create_index(op.f('ix_messages_is_rbl_listed'), 'messages', ['is_rbl_listed'], unique=False)
    op.create_index(op.f('ix_messages_is_spam'), 'messages', ['is_spam'], unique=False)
    op.create_index(op.f('ix_messages_mailscanner_hostname'), 'messages', ['mailscanner_hostname'], unique=False)
    op.create_index(op.f('ix_messages_scanned'), 'messages', ['scanned'], unique=False)
    op.create_index(op.f('ix_messages_stored'), 'messages', ['stored'], unique=False)
    op.create_index(op.f('ix_messages_subject'), 'messages', ['subject'], unique=False)
    op.create_index(op.f('ix_messages_timestamp'), 'messages', ['timestamp'], unique=False)
    op.create_index(op.f('ix_messages_to_address'), 'messages', ['to_address'], unique=False)
    op.create_index(op.f('ix_messages_to_domain'), 'messages', ['to_domain'], unique=False)
    op.create_index(op.f('ix_messages_uuid'), 'messages', ['uuid'], unique=False)
    op.create_table('smtp_relays',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('ip_address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('hostname', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('comment', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_smtp_relays_hostname'), 'smtp_relays', ['hostname'], unique=False)
    op.create_index(op.f('ix_smtp_relays_ip_address'), 'smtp_relays', ['ip_address'], unique=False)
    op.create_index(op.f('ix_smtp_relays_uuid'), 'smtp_relays', ['uuid'], unique=False)
    op.create_table('spamassassin_rule_descriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('key', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('value', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key'),
    sa.UniqueConstraint('value')
    )
    op.create_index(op.f('ix_spamassassin_rule_descriptions_uuid'), 'spamassassin_rule_descriptions', ['uuid'], unique=False)
    op.create_table('spamassassin_rules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('score', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_spamassassin_rules_uuid'), 'spamassassin_rules', ['uuid'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('role', sa.Enum('USER', 'DOMAIN_ADMINISTRATOR', 'SUPERUSER', name='userrole'), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_uuid'), 'users', ['uuid'], unique=False)
    op.create_table('message_headers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('key', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('value', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_headers_message_id'), 'message_headers', ['message_id'], unique=False)
    op.create_index(op.f('ix_message_headers_uuid'), 'message_headers', ['uuid'], unique=False)
    op.create_table('message_mcp_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('contents', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_mcp_reports_message_id'), 'message_mcp_reports', ['message_id'], unique=False)
    op.create_index(op.f('ix_message_mcp_reports_uuid'), 'message_mcp_reports', ['uuid'], unique=False)
    op.create_table('message_rbl_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('contents', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_rbl_reports_message_id'), 'message_rbl_reports', ['message_id'], unique=False)
    op.create_index(op.f('ix_message_rbl_reports_uuid'), 'message_rbl_reports', ['uuid'], unique=False)
    op.create_table('message_spam_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('rule', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('score', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_spam_reports_message_id'), 'message_spam_reports', ['message_id'], unique=False)
    op.create_index(op.f('ix_message_spam_reports_uuid'), 'message_spam_reports', ['uuid'], unique=False)
    op.create_table('message_transport_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('transport_host', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('relay_host', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('transport_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('dsn', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('dsn_message', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('delay', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_transport_log_dsn'), 'message_transport_log', ['dsn'], unique=False)
    op.create_index(op.f('ix_message_transport_log_dsn_message'), 'message_transport_log', ['dsn_message'], unique=False)
    op.create_index(op.f('ix_message_transport_log_message_id'), 'message_transport_log', ['message_id'], unique=False)
    op.create_index(op.f('ix_message_transport_log_relay_host'), 'message_transport_log', ['relay_host'], unique=False)
    op.create_index(op.f('ix_message_transport_log_timestamp'), 'message_transport_log', ['timestamp'], unique=False)
    op.create_index(op.f('ix_message_transport_log_transport_host'), 'message_transport_log', ['transport_host'], unique=False)
    op.create_index(op.f('ix_message_transport_log_transport_type'), 'message_transport_log', ['transport_type'], unique=False)
    op.create_index(op.f('ix_message_transport_log_uuid'), 'message_transport_log', ['uuid'], unique=False)
    op.create_table('user_domains',
    sa.Column('domain_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['domain_id'], ['domains.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('domain_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_domains')
    op.drop_index(op.f('ix_message_transport_log_uuid'), table_name='message_transport_log')
    op.drop_index(op.f('ix_message_transport_log_transport_type'), table_name='message_transport_log')
    op.drop_index(op.f('ix_message_transport_log_transport_host'), table_name='message_transport_log')
    op.drop_index(op.f('ix_message_transport_log_timestamp'), table_name='message_transport_log')
    op.drop_index(op.f('ix_message_transport_log_relay_host'), table_name='message_transport_log')
    op.drop_index(op.f('ix_message_transport_log_message_id'), table_name='message_transport_log')
    op.drop_index(op.f('ix_message_transport_log_dsn_message'), table_name='message_transport_log')
    op.drop_index(op.f('ix_message_transport_log_dsn'), table_name='message_transport_log')
    op.drop_table('message_transport_log')
    op.drop_index(op.f('ix_message_spam_reports_uuid'), table_name='message_spam_reports')
    op.drop_index(op.f('ix_message_spam_reports_message_id'), table_name='message_spam_reports')
    op.drop_table('message_spam_reports')
    op.drop_index(op.f('ix_message_rbl_reports_uuid'), table_name='message_rbl_reports')
    op.drop_index(op.f('ix_message_rbl_reports_message_id'), table_name='message_rbl_reports')
    op.drop_table('message_rbl_reports')
    op.drop_index(op.f('ix_message_mcp_reports_uuid'), table_name='message_mcp_reports')
    op.drop_index(op.f('ix_message_mcp_reports_message_id'), table_name='message_mcp_reports')
    op.drop_table('message_mcp_reports')
    op.drop_index(op.f('ix_message_headers_uuid'), table_name='message_headers')
    op.drop_index(op.f('ix_message_headers_message_id'), table_name='message_headers')
    op.drop_table('message_headers')
    op.drop_index(op.f('ix_users_uuid'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_spamassassin_rules_uuid'), table_name='spamassassin_rules')
    op.drop_table('spamassassin_rules')
    op.drop_index(op.f('ix_spamassassin_rule_descriptions_uuid'), table_name='spamassassin_rule_descriptions')
    op.drop_table('spamassassin_rule_descriptions')
    op.drop_index(op.f('ix_smtp_relays_uuid'), table_name='smtp_relays')
    op.drop_index(op.f('ix_smtp_relays_ip_address'), table_name='smtp_relays')
    op.drop_index(op.f('ix_smtp_relays_hostname'), table_name='smtp_relays')
    op.drop_table('smtp_relays')
    op.drop_index(op.f('ix_messages_uuid'), table_name='messages')
    op.drop_index(op.f('ix_messages_to_domain'), table_name='messages')
    op.drop_index(op.f('ix_messages_to_address'), table_name='messages')
    op.drop_index(op.f('ix_messages_timestamp'), table_name='messages')
    op.drop_index(op.f('ix_messages_subject'), table_name='messages')
    op.drop_index(op.f('ix_messages_stored'), table_name='messages')
    op.drop_index(op.f('ix_messages_scanned'), table_name='messages')
    op.drop_index(op.f('ix_messages_mailscanner_hostname'), table_name='messages')
    op.drop_index(op.f('ix_messages_is_spam'), table_name='messages')
    op.drop_index(op.f('ix_messages_is_rbl_listed'), table_name='messages')
    op.drop_index(op.f('ix_messages_is_mcp'), table_name='messages')
    op.drop_index(op.f('ix_messages_infected'), table_name='messages')
    op.drop_index(op.f('ix_messages_from_domain'), table_name='messages')
    op.drop_index(op.f('ix_messages_from_address'), table_name='messages')
    op.drop_index(op.f('ix_messages_date'), table_name='messages')
    op.drop_index(op.f('ix_messages_client_ip'), table_name='messages')
    op.drop_index(op.f('ix_messages_blocked'), table_name='messages')
    op.drop_index(op.f('ix_messages_allowed'), table_name='messages')
    op.drop_table('messages')
    op.drop_index(op.f('ix_mailscanner_hosts_uuid'), table_name='mailscanner_hosts')
    op.drop_index(op.f('ix_mailscanner_hosts_ip_address'), table_name='mailscanner_hosts')
    op.drop_table('mailscanner_hosts')
    op.drop_index(op.f('ix_list_entries_uuid'), table_name='list_entries')
    op.drop_index(op.f('ix_list_entries_to_domain'), table_name='list_entries')
    op.drop_index(op.f('ix_list_entries_to_address'), table_name='list_entries')
    op.drop_index(op.f('ix_list_entries_listing_type'), table_name='list_entries')
    op.drop_index(op.f('ix_list_entries_from_domain'), table_name='list_entries')
    op.drop_index(op.f('ix_list_entries_from_address'), table_name='list_entries')
    op.drop_table('list_entries')
    op.drop_index(op.f('ix_domains_uuid'), table_name='domains')
    op.drop_index(op.f('ix_domains_name'), table_name='domains')
    op.drop_table('domains')
    # ### end Alembic commands ###