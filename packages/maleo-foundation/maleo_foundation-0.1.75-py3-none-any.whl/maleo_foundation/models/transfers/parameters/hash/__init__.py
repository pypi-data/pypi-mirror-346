from __future__ import annotations
from .bcrypt import BaseBcryptHashParametersTransfers
from .hmac import BaseHMACHashParametersTransfers
from .sha256 import BaseSHA256HashParametersTransfers

class BaseHashParametersTransfers:
    Bcrypt = BaseBcryptHashParametersTransfers
    HMAC = BaseHMACHashParametersTransfers
    SHA256 = BaseSHA256HashParametersTransfers