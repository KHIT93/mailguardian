import logging
from dotenv import load_dotenv
from pathlib import Path
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, validator, AnyHttpUrl, EmailStr, HttpUrl, Field
from typing import Any, Dict, List, Optional, Union, Literal

APP_VERSION = '3.0.0'
API_VERSION = '2.0.0'

BASE_DIR: Path = Path(__file__).parent.parent
ENV_FILE: Path = Path(BASE_DIR.parent, '.env')
ALLOWED_MTAS: List[str] = ['postfix']

# TODO: Find out if HS256 is secure enough for our JWT tokens or if something is better to use
TOKEN_ALGORITHM: str = 'HS256'

load_dotenv(ENV_FILE)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding='utf-8', case_sensitive=False)
    API_ROOT: str = '/api/v2'
    SECRET_KEY: str
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = 'MailGuardian'
    SERVER_HOST: AnyHttpUrl = 'http://localhost'
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:3000', 'http://localhost:8000']

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Union[Optional[PostgresDsn], Optional[str]] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT", 5432),
            path=f"{values.get('POSTGRES_DB') or ''}",
        ).unicode_string()

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return 'MailGuardian'
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_SRC: Path = Path(BASE_DIR, 'resources', 'email', 'src')
    EMAIL_TEMPLATES_DIR: Path = Path(BASE_DIR, 'resources', 'email', 'dist')
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    # Required directories
    TMP_DIR: Path = Path('/tmp')
    CONF_DIR: Path = Path(BASE_DIR, 'configuration')

    # MTA configuration
    MTA: str = 'postfix'
    @validator('MTA', pre=True)
    def validate_mta_is_supported(cls, v: str) -> str:
        if v in ALLOWED_MTAS:
            return v
        else:
            raise ValueError(f'MTA {v} is not supported. Supported MTA are the following: {" ".join(ALLOWED_MTAS)}')
    MTA_LOGFILE: Path = Path('/var/log/maillog')
    SENDMAIL_BIN: Path = Path('/usr/sbin/sendmail')
    POSTQUEUE_BIN: Path = Path('/usr/sbin/postqueue')

    # Audit and retention
    AUDIT_LOGGING: bool = True
    RECORD_RETENTION: int = 60
    AUDIT_RETENTION: int = 60
    QUARANTINE_RETENTION: int = 60

    # Branding
    BRAND_NAME: str = 'MailGuardian'
    BRAND_TAGLINE: str = 'Securing your email'
    BRAND_LOGO: str = ''
    BRAND_SUPPORT: HttpUrl = 'https://github.com/khit93/mailguardian/issues'
    BRAND_FEEDBACK: HttpUrl = 'https://github.com/khit93/mailguardian/issues'

    # GeoIP
    MAXMIND_DB_PATH: Path = Path(BASE_DIR, 'run')
    MAXMIND_DB_FILE: Path = Path(MAXMIND_DB_PATH, 'GeoLite2.mmdb')
    MAXMIND_ACCOUNT_API_KEY: Optional[str] = Field(default=None)

    #MailScanner settings
    MAILSCANNER_BIN: Path = Path('/usr/sbin/MailScanner')
    MAILSCANNER_CONFIG_DIR: Path = Path('/etc/MailScanner')
    MAILSCANNER_SHARE_DIR: Path = Path('/usr/share/MailScanner')
    MAILSCANNER_LIB_DIR: Path = Path('/usr/lib/MailScanner')
    MAILSCANNER_QUARANTINE_DIR: Path = Path('/var/spool/MailScanner/quarantine')

    # SpamAssassin settings
    SALEARN_BIN: Path = Path('/usr/bin/salearn')
    SA_BIN: Path = Path('/usr/bin/spamassassin')
    SA_RULES_DIR: Path = Path('/usr/share/spamassassin')
    SA_PREF: Path = Path(MAILSCANNER_CONFIG_DIR, '/spamassassin.conf')

    STORAGE_DIR: Path = Path(BASE_DIR, 'storage')

    # Application logging
    APP_LOG_TO_FILE: bool = Field(default=True)
    APP_LOGFILE: Optional[Path] = Field(default=Path(STORAGE_DIR, 'logs', 'mailguardian.app.log'))
    APP_LOGLEVEL: int = Field(default=logging.INFO)

    # Security
    APP_ENFORCE_MFA: bool = Field(default=True)
    


settings = Settings()