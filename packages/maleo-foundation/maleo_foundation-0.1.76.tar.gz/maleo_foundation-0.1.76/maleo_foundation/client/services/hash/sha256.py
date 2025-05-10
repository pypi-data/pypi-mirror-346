from Crypto.Hash import SHA256
from maleo_foundation.expanded_types.hash import BaseHashResultsTypes
from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.models.schemas.hash import BaseHashSchemas
from maleo_foundation.models.transfers.parameters.hash.sha256 import BaseSHA256HashParametersTransfers
from maleo_foundation.models.transfers.results.hash import BaseHashResultsTransfers
from maleo_foundation.utils.exceptions import BaseExceptions

class MaleoFoundationSHA256HashClientService(ClientService):
    def hash(self, parameters:BaseSHA256HashParametersTransfers.Hash) -> BaseHashResultsTypes.Hash:
        """Generate a sha256 hash for the given message."""
        @BaseExceptions.service_exception_handler(
            operation="hashing single message",
            logger=self._logger,
            fail_result_class=BaseHashResultsTransfers.Fail
        )
        def _impl():
            hash = SHA256.new(parameters.message.encode()).hexdigest()
            data = BaseHashSchemas.Hash(hash=hash)
            self._logger.info("Message successfully hashed")
            return BaseHashResultsTransfers.Hash(data=data)
        return _impl()

    def verify(self, parameters:BaseSHA256HashParametersTransfers.Verify) -> BaseHashResultsTypes.Verify:
        """Verify a message against the given message hash."""
        @BaseExceptions.service_exception_handler(
            operation="verify single hash",
            logger=self._logger,
            fail_result_class=BaseHashResultsTransfers.Fail
        )
        def _impl():
            computed_hash = SHA256.new(parameters.message.encode()).hexdigest()
            is_valid = computed_hash == parameters.hash
            data = BaseHashSchemas.IsValid(is_valid=is_valid)
            self._logger.info("Hash successfully verified")
            return BaseHashResultsTransfers.Verify(data=data)
        return _impl()