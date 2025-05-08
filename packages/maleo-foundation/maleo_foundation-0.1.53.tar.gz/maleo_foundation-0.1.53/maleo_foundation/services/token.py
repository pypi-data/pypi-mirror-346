import jwt
from maleo_foundation.models.transfers.general.token import BaseTokenGeneralTransfers
from maleo_foundation.models.schemas.token import BaseTokenSchemas
from maleo_foundation.models.transfers.parameters.token import BaseTokenParametersTransfers
from maleo_foundation.models.transfers.results.token import BaseTokenResultsTransfers
from maleo_foundation.expanded_types.token import BaseTokenResultsTypes

class BaseTokenService:
    @staticmethod
    def encode(parameters:BaseTokenParametersTransfers.Encode) -> BaseTokenResultsTypes.Encode:
        payload = BaseTokenGeneralTransfers.EncodePayload.model_validate(parameters.payload.model_dump()).model_dump(mode="json")
        token = jwt.encode(payload=payload, key=parameters.key.encode(), algorithm="RS256")
        data = BaseTokenSchemas.Token(token=token)
        return BaseTokenResultsTransfers.Encode(data=data)

    @staticmethod
    def decode(parameters:BaseTokenParametersTransfers.Decode) -> BaseTokenResultsTypes.Decode:
        payload = jwt.decode(jwt=parameters.token, key=parameters.key, algorithms=["RS256"])
        data = BaseTokenGeneralTransfers.DecodePayload.model_validate(payload)
        return BaseTokenResultsTransfers.Decode(data=data)