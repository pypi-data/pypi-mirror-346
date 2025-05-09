from __future__ import annotations
from maleo_foundation.managers.client.base import ClientManager
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.logging import SimpleConfig
from maleo_foundation.client.services.hash import (
    MaleoFoundationSHA256HashClientService,
    MaleoFoundationHMACHashClientService,
    MaleoFoundationBcryptHashClientService
)
from maleo_foundation.client.services import (
    MaleoFoundationHashServices,
    MaleoFoundationSignatureClientService,
    MaleoFoundationTokenClientService,
    MaleoFoundationServices
)

class MaleoFoundationClientManager(ClientManager):
    def __init__(self, log_config:SimpleConfig, service_key:BaseTypes.OptionalString=None):
        key = "maleo-foundation"
        name = "MaleoFoundation"
        super().__init__(key, name, log_config, service_key)
        self._initialize_services()
        self._logger.info("Client manager initialized successfully")

    def _initialize_services(self):
        super()._initialize_services()
        bcrypt_hash_service = MaleoFoundationBcryptHashClientService(logger=self._logger)
        hmac_hash_service = MaleoFoundationHMACHashClientService(logger=self._logger)
        sha256_hash_service = MaleoFoundationSHA256HashClientService(logger=self._logger)
        hash_services = MaleoFoundationHashServices(
            bcrypt=bcrypt_hash_service,
            hmac=hmac_hash_service,
            sha256=sha256_hash_service
        )
        signature_service = MaleoFoundationSignatureClientService(logger=self._logger)
        token_service = MaleoFoundationTokenClientService(logger=self._logger)
        self._services = MaleoFoundationServices(
            signature=signature_service,
            token=token_service,
            hash=hash_services
        )

    @property
    def services(self) -> MaleoFoundationServices:
        return self._services