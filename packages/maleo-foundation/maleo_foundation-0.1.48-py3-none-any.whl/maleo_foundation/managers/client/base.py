from maleo_foundation.utils.logging import ClientLogger
from maleo_foundation.managers.service import ServiceManager

class ClientManager:
    def __init__(
        self,
        key:str,
        name:str,
        service_manager:ServiceManager
    ) -> None:
        self._key = key
        self._name = name
        self._service_manager = service_manager
        self._initialize_logger()
        self._logger.info("Initializing client manager")

    def _initialize_logger(self) -> None:
        self._logger = ClientLogger(client_key=self._key, service_key=self._service_manager.configs.service.key, **self._service_manager.log_config.model_dump())

    @property
    def key(self) -> str:
        return self._key

    @property
    def name(self) -> str:
        return self._name

    @property
    def service_manager(self) -> ServiceManager:
        return self._service_manager

    @property
    def logger(self) -> ClientLogger:
        return self._logger

    @property
    def credentials(self):
        raise NotImplementedError()

    @property
    def client(self):
        raise NotImplementedError()