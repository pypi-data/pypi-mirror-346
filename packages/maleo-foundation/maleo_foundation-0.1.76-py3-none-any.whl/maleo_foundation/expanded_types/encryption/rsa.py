from typing import Union
from maleo_foundation.models.transfers.results.encryption.rsa import BaseRSAEncryptionResultsTransfers

class BaseRSAEncryptionResultsTypes:
    Encrypt = Union[
        BaseRSAEncryptionResultsTransfers.Fail,
        BaseRSAEncryptionResultsTransfers.Encrypt
    ]

    Decrypt = Union[
        BaseRSAEncryptionResultsTransfers.Fail,
        BaseRSAEncryptionResultsTransfers.Decrypt
    ]