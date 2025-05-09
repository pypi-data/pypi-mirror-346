from maleo_foundation.models.schemas.signature import BaseSignatureSchemas

class BaseSignatureParametersTransfers:
    class Sign(
        BaseSignatureSchemas.Message,
        BaseSignatureSchemas.Password,
        BaseSignatureSchemas.Key
    ): pass

    class Verify(
        BaseSignatureSchemas.Signature,
        BaseSignatureSchemas.Message,
        BaseSignatureSchemas.Key
    ): pass