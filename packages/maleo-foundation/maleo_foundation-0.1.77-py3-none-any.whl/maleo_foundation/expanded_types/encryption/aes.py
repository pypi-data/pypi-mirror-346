from typing import Union
from maleo_foundation.models.transfers.results.encryption.aes import BaseAESEncryptionResultsTransfers

class BaseAESEncryptionResultsTypes:
    Encrypt = Union[
        BaseAESEncryptionResultsTransfers.Fail,
        BaseAESEncryptionResultsTransfers.Encrypt
    ]

    Decrypt = Union[
        BaseAESEncryptionResultsTransfers.Fail,
        BaseAESEncryptionResultsTransfers.Decrypt
    ]