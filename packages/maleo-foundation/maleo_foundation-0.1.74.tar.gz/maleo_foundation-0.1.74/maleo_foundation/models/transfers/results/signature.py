from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_foundation.models.schemas.signature import BaseSignatureSchemas

class BaseSignatureResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class Sign(BaseServiceGeneralResultsTransfers.SingleData):
        data:BaseSignatureSchemas.Signature = Field(..., description="Single signature data")

    class Verify(BaseServiceGeneralResultsTransfers.SingleData):
        data:BaseSignatureSchemas.IsValid = Field(..., description="Single verify data")