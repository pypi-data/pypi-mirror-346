from typing import Union
from maleo_foundation.models.transfers.results.key import BaseKeyResultsTransfers

class BaseKeyResultsTypes:
    CreatePrivate = Union[
        BaseKeyResultsTransfers.Fail,
        BaseKeyResultsTransfers.CreatePrivate
    ]

    CreatePublic = Union[
        BaseKeyResultsTransfers.Fail,
        BaseKeyResultsTransfers.CreatePublic
    ]

    CreatePair = Union[
        BaseKeyResultsTransfers.Fail,
        BaseKeyResultsTransfers.CreatePair
    ]