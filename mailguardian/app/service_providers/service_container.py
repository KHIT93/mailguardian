import logging

from fastapi_mail import FastMail
from injector import Injector, Module, provider, singleton

from mailguardian.config.mail import config as mail_config
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

    @provider
    def provide_email(self) -> FastMail:
        self._logger.info('Providing email processing')
        return FastMail(mail_config)


def setup_service_container() -> Injector:
    return Injector([ServiceContainer()])


# Configure Dependency Injection
services: Injector = setup_service_container()
