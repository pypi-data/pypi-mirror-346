import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from maleo_foundation.models.transfers.general.token import BaseTokenGeneralTransfers
from maleo_foundation.models.schemas.token import BaseTokenSchemas
from maleo_foundation.models.transfers.parameters.token import BaseTokenParametersTransfers
from maleo_foundation.models.transfers.results.token import BaseTokenResultsTransfers
from maleo_foundation.expanded_types.token import BaseTokenResultsTypes

class BaseTokenService:
    @staticmethod
    def encode(parameters:BaseTokenParametersTransfers.Encode) -> BaseTokenResultsTypes.Encode:
        #* Serialize private key
        private_key_bytes = parameters.key.encode()
        private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=parameters.password.encode() if parameters.password else None,
            backend=default_backend()
        )
        payload = BaseTokenGeneralTransfers.EncodePayload.model_validate(parameters.payload.model_dump()).model_dump(mode="json")
        token = jwt.encode(payload=payload, key=private_key, algorithm="RS256")
        data = BaseTokenSchemas.Token(token=token)
        return BaseTokenResultsTransfers.Encode(data=data)

    @staticmethod
    def decode(parameters:BaseTokenParametersTransfers.Decode) -> BaseTokenResultsTypes.Decode:
        payload = jwt.decode(jwt=parameters.token, key=parameters.key, algorithms=["RS256"])
        data = BaseTokenGeneralTransfers.DecodePayload.model_validate(payload)
        return BaseTokenResultsTransfers.Decode(data=data)