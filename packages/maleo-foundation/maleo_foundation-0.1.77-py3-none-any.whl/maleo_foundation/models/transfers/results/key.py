from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_foundation.models.transfers.general.key import BaseKeyGeneralTransfers

class BaseKeyResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class CreatePrivate(BaseServiceGeneralResultsTransfers.SingleData):
        data:BaseKeyGeneralTransfers.PrivateKey = Field(..., description="Private key data")

    class CreatePublic(BaseServiceGeneralResultsTransfers.SingleData):
        data:BaseKeyGeneralTransfers.PublicKey = Field(..., description="Private key data")

    class CreatePair(BaseServiceGeneralResultsTransfers.SingleData):
        data:BaseKeyGeneralTransfers.KeyPair = Field(..., description="Key pair data")