from maleo_foundation.models.schemas.hash import BaseHashSchemas

class BaseSHA256HashParametersTransfers:
    class Hash(BaseHashSchemas.Message): pass

    class Verify(
        BaseHashSchemas.Hash,
        BaseHashSchemas.Message
    ): pass