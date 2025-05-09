from typing import Union
from maleo_foundation.models.transfers.results.hash import BaseHashResultsTransfers

class BaseHashResultsTypes:
    Hash = Union[
        BaseHashResultsTransfers.Fail,
        BaseHashResultsTransfers.Hash
    ]

    Verify = Union[
        BaseHashResultsTransfers.Fail,
        BaseHashResultsTransfers.Verify
    ]