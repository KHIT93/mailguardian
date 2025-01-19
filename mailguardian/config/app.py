import logging
import string
from dotenv import load_dotenv
from pathlib import Path
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BeforeValidator, PostgresDsn, model_validator, validator, AnyHttpUrl, EmailStr, HttpUrl, Field, computed_field
from typing import Annotated, Any, Dict, List, Optional, Union, Literal
from typing_extensions import Self
from distutils.util import strtobool

APP_VERSION = '3.0.0'
API_VERSION = '2.0.0'

BASE_DIR: Path = Path(__file__).parent.parent
ENV_FILE: Path = Path(BASE_DIR.parent, '.env')
ALLOWED_MTAS: List[str] = ['postfix']

# TODO: Find out if HS256 is secure enough for our JWT tokens or if something is better to use
TOKEN_ALGORITHM: str = 'HS256'

RANDOM_CHARACTER_DATA: list[str] = list(string.ascii_letters + string.digits + string.punctuation.replace('"','').replace('\'',''))

# load_dotenv(ENV_FILE)

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    API_ROOT: str = '/api/v2'
    SECRET_KEY: str
    # 60 minutes * 24 hours = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    SERVER_NAME: str = 'MailGuardian'
    SERVER_HOST: AnyHttpUrl = 'http://localhost'
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyHttpUrl] | str, BeforeValidator(parse_cors)
    ] = ['http://localhost:3000', 'http://localhost:8000']

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = "MailGuardian"

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.SERVER_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_SRC: Path = Path(BASE_DIR, 'resources', 'email', 'src')
    EMAIL_TEMPLATES_DIR: Path = Path(BASE_DIR, 'resources', 'email', 'dist')

    @computed_field  # type: ignore[prop-decorator]
    @property
    def EMAILS_ENABLED(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    # Required directories
    TMP_DIR: Path = Path('/tmp')
    CONF_DIR: Path = Path(BASE_DIR, 'configuration')

    # MTA configuration
    MTA: str = 'postfix'

    @model_validator(mode="after")
    def validate_mta_is_supported(self) -> Self:
        if self.MTA not in ALLOWED_MTAS:
            raise ValueError(f'MTA {self.MTA} is not supported. Supported MTA are the following: {" ".join(ALLOWED_MTAS)}')
        return self
    
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
    APP_LOG_TO_FILE: bool = True
    APP_LOGFILE: Optional[Path] = Field(default=Path(STORAGE_DIR, 'logs', 'mailguardian.app.log'))
    APP_LOGLEVEL: int = logging.INFO

    # Security
    APP_ENFORCE_MFA: bool = True
    
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding='utf-8', case_sensitive=False, extra='ignore')


settings = Settings()