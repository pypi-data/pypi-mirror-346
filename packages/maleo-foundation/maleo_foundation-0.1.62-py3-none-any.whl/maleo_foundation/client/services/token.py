import jwt
from maleo_foundation.models.schemas.token import BaseTokenSchemas
from maleo_foundation.models.transfers.general.token import BaseTokenGeneralTransfers
from maleo_foundation.models.transfers.parameters.token import BaseTokenParametersTransfers
from maleo_foundation.models.transfers.results.token import BaseTokenResultsTransfers
from maleo_foundation.expanded_types.token import BaseTokenResultsTypes
from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.utils.exceptions import BaseExceptions

class MaleoFoundationTokenClientService(ClientService):
    def encode(self, parameters:BaseTokenParametersTransfers.Encode) -> BaseTokenResultsTypes.Encode:
        @BaseExceptions.service_exception_handler(
            operation="encoding a payload into a token",
            logger=self._logger,
            fail_result_class=BaseTokenResultsTransfers.Fail
        )
        def _impl():
            payload = BaseTokenGeneralTransfers.EncodePayload.model_validate(parameters.payload.model_dump()).model_dump(mode="json")
            token = jwt.encode(payload=payload, key=parameters.key, algorithm="RS256")
            data = BaseTokenSchemas.Token(token=token)
            return BaseTokenResultsTransfers.Encode(data=data)
        return _impl()

    def decode(self, parameters:BaseTokenParametersTransfers.Decode) -> BaseTokenResultsTypes.Decode:
        @BaseExceptions.service_exception_handler(
            operation="decoding a token into a payload",
            logger=self._logger,
            fail_result_class=BaseTokenResultsTransfers.Fail
        )
        def _impl():
            payload = jwt.decode(jwt=parameters.token, key=parameters.key, algorithms=["RS256"])
            data = BaseTokenGeneralTransfers.DecodePayload.model_validate(payload)
            return BaseTokenResultsTransfers.Decode(data=data)
        return _impl()