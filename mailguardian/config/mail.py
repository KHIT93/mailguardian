from pathlib import Path

from fastapi_mail import ConnectionConfig

from mailguardian.config.app import BASE_DIR

config: ConnectionConfig = ConnectionConfig(
    MAIL_USERNAME='',
    MAIL_PASSWORD='',
    MAIL_PORT=25,
    MAIL_SERVER='localhost',
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    TEMPLATE_FOLDER=Path(BASE_DIR, 'resources', 'email')
)
