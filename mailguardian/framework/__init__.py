import logging

from injector import Module, provider, Injector, inject, singleton

from mailguardian.config.app import settings
from mailguardian.database.connect import Database

class ServiceContainer(Module):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info('Bootstrapping Service Container')

    @singleton
    @provider
    def provide_database(self) -> Database:
        self._logger.info('Providing a database connection')
        return Database()
    
def setup_service_container() -> Injector:
    return Injector([ServiceContainer()])