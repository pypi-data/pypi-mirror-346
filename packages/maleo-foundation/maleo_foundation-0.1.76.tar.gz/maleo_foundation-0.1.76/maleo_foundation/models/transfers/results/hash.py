from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_foundation.models.schemas.hash import BaseHashSchemas

class BaseHashResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class Hash(BaseServiceGeneralResultsTransfers.SingleData):
        data:BaseHashSchemas.Hash = Field(..., description="Hash data")

    class Verify(BaseServiceGeneralResultsTransfers.SingleData):
        data:BaseHashSchemas.IsValid = Field(..., description="Verify data")