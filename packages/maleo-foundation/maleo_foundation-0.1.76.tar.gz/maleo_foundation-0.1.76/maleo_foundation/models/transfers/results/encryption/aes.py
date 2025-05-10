from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_foundation.models.schemas.encryption import BaseEncryptionSchemas

class EncryptData(
    BaseEncryptionSchemas.Ciphertext,
    BaseEncryptionSchemas.InitializationVector,
    BaseEncryptionSchemas.Key
): pass

class BaseAESEncryptionResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class Encrypt(BaseServiceGeneralResultsTransfers.SingleData):
        data:EncryptData = Field(..., description="Single encryption data")

    class Decrypt(BaseServiceGeneralResultsTransfers.SingleData):
        data:BaseEncryptionSchemas.Plaintext = Field(..., description="Single decryption data")