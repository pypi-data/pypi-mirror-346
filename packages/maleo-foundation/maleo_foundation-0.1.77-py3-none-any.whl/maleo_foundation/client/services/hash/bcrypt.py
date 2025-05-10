import bcrypt
from maleo_foundation.expanded_types.hash import BaseHashResultsTypes
from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.models.schemas.hash import BaseHashSchemas
from maleo_foundation.models.transfers.parameters.hash.bcrypt import BaseBcryptHashParametersTransfers
from maleo_foundation.models.transfers.results.hash import BaseHashResultsTransfers
from maleo_foundation.utils.exceptions import BaseExceptions

class MaleoFoundationBcryptHashClientService(ClientService):
    def hash(self, parameters:BaseBcryptHashParametersTransfers.Hash) -> BaseHashResultsTypes.Hash:
        """Generate a bcrypt hash for the given message."""
        @BaseExceptions.service_exception_handler(
            operation="hashing single message",
            logger=self._logger,
            fail_result_class=BaseHashResultsTransfers.Fail
        )
        def _impl():
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(parameters.message.encode(), salt).decode()
            data = BaseHashSchemas.Hash(hash=hash)
            self._logger.info("Message successfully hashed")
            return BaseHashResultsTransfers.Hash(data=data)
        return _impl()

    def verify(self, parameters:BaseBcryptHashParametersTransfers.Verify) -> BaseHashResultsTypes.Verify:
        """Verify a message against the given message hash."""
        @BaseExceptions.service_exception_handler(
            operation="verify single hash",
            logger=self._logger,
            fail_result_class=BaseHashResultsTransfers.Fail
        )
        def _impl():
            is_valid = bcrypt.checkpw(parameters.message.encode(), parameters.hash.encode())
            data = BaseHashSchemas.IsValid(is_valid=is_valid)
            self._logger.info("Hash successfully verified")
            return BaseHashResultsTransfers.Verify(data=data)
        return _impl()