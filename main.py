from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

# from mailguardian.app import api_routes, web_routes
from mailguardian.app.bootstrap.routes import register_api_routes, register_web_routes
from mailguardian.app.http.middleware import middleware as http_middleware
from mailguardian.config.app import API_VERSION, settings

api_routes: list[APIRouter] = register_api_routes()
web_routes: list = register_web_routes()


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    # On Startup
    # init_logger(level=settings.APP_LOGLEVEL)
    # if settings.APP_LOGFILE and settings.APP_LOG_TO_FILE:
    #     enable_logfile(filename=settings.APP_LOGFILE)
    # else:
    #     enable_stdout_logging()
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

# for route in web_routes:
# DO SOMETHING
for route in api_routes:
    app.include_router(route)

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
