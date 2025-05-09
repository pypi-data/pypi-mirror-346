from __future__ import annotations
from maleo_foundation.models.schemas.signature import BaseSignatureSchemas

class BaseSignatureGeneralTransfers:
    class SignaturePackage(
        BaseSignatureSchemas.Message,
        BaseSignatureSchemas.Signature
    ): pass