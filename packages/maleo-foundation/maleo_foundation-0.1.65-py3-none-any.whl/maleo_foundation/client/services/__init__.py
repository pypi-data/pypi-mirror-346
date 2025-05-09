from __future__ import annotations
from pydantic import Field
from maleo_foundation.managers.client.base import ClientServices
from maleo_foundation.client.services.signature import MaleoFoundationSignatureClientService
from maleo_foundation.client.services.token import MaleoFoundationTokenClientService

class MaleoFoundationServices(ClientServices):
    signature:MaleoFoundationSignatureClientService = Field(..., description="Signature's service")
    token:MaleoFoundationTokenClientService = Field(..., description="Token's service")