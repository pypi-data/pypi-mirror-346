from __future__ import annotations
from .aes import BaseAESEncryptionResultsTransfers
from .rsa import BaseRSAEncryptionResultsTransfers

class BaseEncryptionResultsTypes:
    AES = BaseAESEncryptionResultsTransfers
    RSA = BaseRSAEncryptionResultsTransfers