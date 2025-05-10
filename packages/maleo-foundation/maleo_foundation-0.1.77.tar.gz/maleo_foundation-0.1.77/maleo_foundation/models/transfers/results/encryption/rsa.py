from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_foundation.models.schemas.encryption import BaseEncryptionSchemas

class BaseRSAEncryptionResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class Encrypt(BaseServiceGeneralResultsTransfers.SingleData):
        data:BaseEncryptionSchemas.Ciphertext = Field(..., description="Single encryption data")

    class Decrypt(BaseServiceGeneralResultsTransfers.SingleData):
        data:BaseEncryptionSchemas.Plaintext = Field(..., description="Single decryption data")