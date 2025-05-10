from maleo_foundation.models.schemas.hash import BaseHashSchemas

class BaseBcryptHashParametersTransfers:
    class Hash(BaseHashSchemas.Message): pass

    class Verify(
        BaseHashSchemas.Hash,
        BaseHashSchemas.Message
    ): pass