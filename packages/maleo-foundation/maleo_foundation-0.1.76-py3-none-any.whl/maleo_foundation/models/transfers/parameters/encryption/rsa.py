from maleo_foundation.models.schemas.encryption import BaseEncryptionSchemas

class BaseRSAEncryptionParametersTransfers:
    class Encrypt(
        BaseEncryptionSchemas.Plaintext,
        BaseEncryptionSchemas.Key
    ): pass

    class Decrypt(
        BaseEncryptionSchemas.Ciphertext,
        BaseEncryptionSchemas.Key
    ): pass