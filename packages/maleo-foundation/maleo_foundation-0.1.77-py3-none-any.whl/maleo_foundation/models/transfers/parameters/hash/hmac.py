from maleo_foundation.models.schemas.hash import BaseHashSchemas

class BaseHMACHashParametersTransfers:
    class Hash(
        BaseHashSchemas.Message,
        BaseHashSchemas.Key
    ): pass

    class Verify(
        BaseHashSchemas.Hash,
        BaseHashSchemas.Message,
        BaseHashSchemas.Key
    ): pass