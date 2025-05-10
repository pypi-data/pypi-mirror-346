from pydantic import BaseModel, Field
from starlette.authentication import AuthCredentials, BaseUser
from typing import Optional, Sequence
from maleo_foundation.models.transfers.general.token import MaleoFoundationTokenGeneralTransfers
from maleo_foundation.types import BaseTypes

class Credentials(AuthCredentials):
    def __init__(
        self,
        key:BaseTypes.OptionalString = None,
        token:BaseTypes.OptionalString = None,
        payload:Optional[MaleoFoundationTokenGeneralTransfers.DecodePayload] = None,
        scopes:Optional[Sequence[str]] = None
    ) -> None:
        self._key = key
        self._token = token
        self._payload = payload
        super().__init__(scopes)

    @property
    def key(self) -> BaseTypes.OptionalString:
        return self._key

    @property
    def token(self) -> BaseTypes.OptionalString:
        return self._token

    @property
    def payload(self) -> Optional[MaleoFoundationTokenGeneralTransfers.DecodePayload]:
        return self._payload

class User(BaseUser):
    def __init__(
        self,
        authenticated:bool = True,
        username:str = "",
        email:str = ""
    ) -> None:
        self._authenticated = authenticated
        self._username = username
        self._email = email

    @property
    def is_authenticated(self) -> bool:
        return self._authenticated

    @property
    def display_name(self) -> str:
        return self._username

    @property
    def identity(self) -> str:
        return self._email

class Authentication(BaseModel):
    credentials:Credentials = Field(..., description="Credentials's information")
    user:User = Field(..., description="User's information")

    class Config:
        arbitrary_types_allowed=True