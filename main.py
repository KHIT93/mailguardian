from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from mailguardian.config.app import settings, API_VERSION
from mailguardian.config.logging import customize_fastapi_logger, init_logger, enable_stdout_logging, enable_logfile
from mailguardian.app import models
from mailguardian.database.connect import engine
from mailguardian.app.dependencies import get_database_session
from mailguardian.app.http.middleware import middleware as http_middleware
import logging
import uvicorn
logger = logging.getLogger(__name__)

# Add routers
# TODO: Find a way to only have one import and then have everything else happen in the routes module
from mailguardian.routes.api.audit_log import router as audit_log_router
from mailguardian.routes.api.domains import router as domains_router
from mailguardian.routes.api.auth import router as auth_router
from mailguardian.routes.api.users import router as user_router
from mailguardian.routes.api.blocklist import router as blocklist_router
from mailguardian.routes.api.allowlist import router as allowlist_router
from mailguardian.routes.api.messages import router as message_router
from mailguardian.routes.api.mailscanner_hosts import router as mailscanner_hosts_router
from mailguardian.routes.api.smtp_relays import router as smtp_relay_router
from mailguardian.routes.api.spamassassin_rules import router as sa_rules_router
from mailguardian.routes.api.spamassassin_descriptions import router as sa_rule_descriptions_router

# Application bootstrapping
# TODO: See if we can move this to separate python module and then simply import it here
@asynccontextmanager
async def lifespan(app: FastAPI):
    # On Startup
    init_logger(level=settings.APP_LOGLEVEL)
    if settings.APP_LOGFILE and settings.APP_LOG_TO_FILE:
        enable_logfile(filename=settings.APP_LOGFILE)
    else:
        enable_stdout_logging()
    # customize_fastapi_logger()
    # Init database
    # SQLModel.metadata.create_all(engine)

    yield

    # On Shutdown
    # SQLModel.metadata.drop_all(engine)


# END Application bootstrapping

app = FastAPI(
    title='MailGuardian',
    lifespan=lifespan,
    version=API_VERSION,
    root_path=settings.API_ROOT,
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Not found"},
    },
    middleware=http_middleware
)

app.include_router(auth_router)
app.include_router(domains_router)
app.include_router(user_router)
app.include_router(allowlist_router)
app.include_router(blocklist_router)
app.include_router(message_router)
app.include_router(mailscanner_hosts_router)
app.include_router(smtp_relay_router)
app.include_router(sa_rules_router)
app.include_router(sa_rule_descriptions_router)
app.include_router(audit_log_router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
