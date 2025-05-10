from __future__ import annotations
from .aes import BaseAESEncryptionParametersTransfers
from .rsa import BaseRSAEncryptionParametersTransfers

class BaseEncryptionParametersTransfers:
    AES = BaseAESEncryptionParametersTransfers
    RSA = BaseRSAEncryptionParametersTransfers