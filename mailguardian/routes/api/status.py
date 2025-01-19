
from fastapi import APIRouter, Depends

from mailguardian.app.dependencies import get_database_session

router = APIRouter(
    prefix='/status',
    tags=['Application Status'],
    dependencies=[
        Depends(get_database_session)
    ]
)


@router.get('/ping', summary='Ping the application', description='Healthcheck endpoint to check if the application is running or not')
@router.get('/up', summary='Healthcheck', description='Healthcheck endpoint to check if the application is running or not, but using a known default endpoint')
async def ping() -> str:
    return 'pong'

# @router.get('/ready', response_model=List[Domain], summary='Check if the application is ready', description='Healthcheck endpoint to get information about the state of the application and whether or not it is ready to process requests')
# async def get_domains(db: Annotated[Session, Depends(get_database_session)]) -> List[Domain]:
#     return {}
