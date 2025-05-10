from __future__ import annotations
from .aes import BaseAESEncryptionResultsTransfers
from .rsa import BaseRSAEncryptionResultsTransfers

class BaseEncryptionResultsTransfers:
    AES = BaseAESEncryptionResultsTransfers
    RSA = BaseRSAEncryptionResultsTransfers