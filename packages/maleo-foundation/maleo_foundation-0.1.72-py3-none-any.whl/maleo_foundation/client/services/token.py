import jwt
from maleo_foundation.enums import BaseEnums
from maleo_foundation.expanded_types.token import BaseTokenResultsTypes
from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.models.schemas.token import BaseTokenSchemas
from maleo_foundation.models.transfers.general.token import BaseTokenGeneralTransfers
from maleo_foundation.models.transfers.parameters.token import BaseTokenParametersTransfers
from maleo_foundation.models.transfers.results.token import BaseTokenResultsTransfers
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_foundation.utils.loaders.key.rsa import RSAKeyLoader

class MaleoFoundationTokenClientService(ClientService):
    def encode(self, parameters:BaseTokenParametersTransfers.Encode) -> BaseTokenResultsTypes.Encode:
        @BaseExceptions.service_exception_handler(
            operation="encoding a payload into a token",
            logger=self._logger,
            fail_result_class=BaseTokenResultsTransfers.Fail
        )
        def _impl():
            try:
                private_key = RSAKeyLoader.load_with_pycryptodome(type=BaseEnums.KeyType.PRIVATE, extern_key=parameters.key, passphrase=parameters.password)
            except TypeError:
                message = "Invalid key type"
                description = "A private key must be used for payload encoding"
                other = "Ensure the given key is of type private key"
                return BaseTokenResultsTransfers.Fail(message=message, description=description, other=other)
            except Exception as e:
                self._logger.error("Unexpected error occured while trying to import key:\n'%s'", str(e), exc_info=True)
                message = "Invalid key"
                description = "Unexpected error occured while trying to import key"
                other = "Ensure given key is valid"
                return BaseTokenResultsTransfers.Fail(message=message, description=description, other=other)
            payload = BaseTokenGeneralTransfers.EncodePayload.model_validate(parameters.payload.model_dump()).model_dump(mode="json")
            token = jwt.encode(payload=payload, key=private_key.export_key(), algorithm="RS256")
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
            try:
                public_key = RSAKeyLoader.load_with_pycryptodome(type=BaseEnums.KeyType.PUBLIC, extern_key=parameters.key)
            except TypeError:
                message = "Invalid key type"
                description = "A public key must be used for token decoding"
                other = "Ensure the given key is of type public key"
                return BaseTokenResultsTransfers.Fail(message=message, description=description, other=other)
            except Exception as e:
                self._logger.error("Unexpected error occured while trying to import key:\n'%s'", str(e), exc_info=True)
                message = "Invalid key"
                description = "Unexpected error occured while trying to import key"
                other = "Ensure given key is valid"
                return BaseTokenResultsTransfers.Fail(message=message, description=description, other=other)
            payload = jwt.decode(jwt=parameters.token, key=public_key.export_key(), algorithms=["RS256"])
            data = BaseTokenGeneralTransfers.DecodePayload.model_validate(payload)
            return BaseTokenResultsTransfers.Decode(data=data)
        return _impl()