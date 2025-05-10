from maleo_foundation.models.schemas.encryption import BaseEncryptionSchemas

class BaseAESEncryptionParametersTransfers:
    class Encrypt(
        BaseEncryptionSchemas.Plaintext,
        BaseEncryptionSchemas.Key
    ): pass

    class Decrypt(
        BaseEncryptionSchemas.Ciphertext,
        BaseEncryptionSchemas.InitializationVector,
        BaseEncryptionSchemas.Key
    ): pass