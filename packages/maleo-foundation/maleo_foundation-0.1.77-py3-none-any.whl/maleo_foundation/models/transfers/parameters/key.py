from maleo_foundation.models.schemas.key import BaseKeySchemas
from maleo_foundation.models.transfers.general.key import BaseKeyGeneralTransfers

class BaseKeyParametersTransfers:
    class CreatePrivateOrPair(
        BaseKeySchemas.Password,
        BaseKeySchemas.KeySize
    ): pass

    class CreatePublic(
        BaseKeySchemas.Password,
        BaseKeyGeneralTransfers.PrivateKey
    ): pass