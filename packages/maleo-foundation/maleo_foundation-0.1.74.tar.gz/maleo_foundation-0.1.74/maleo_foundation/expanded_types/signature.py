from typing import Union
from maleo_foundation.models.transfers.results.signature import BaseSignatureResultsTransfers

class BaseSignatureResultsTypes:
    Sign = Union[
        BaseSignatureResultsTransfers.Fail,
        BaseSignatureResultsTransfers.Sign
    ]

    Verify = Union[
        BaseSignatureResultsTransfers.Fail,
        BaseSignatureResultsTransfers.Verify
    ]