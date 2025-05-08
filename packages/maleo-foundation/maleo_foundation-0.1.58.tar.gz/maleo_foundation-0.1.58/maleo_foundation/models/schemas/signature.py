from pydantic import BaseModel, Field

class BaseSignatureSchemas:
    class Key(BaseModel):
        key:str = Field(..., description="Key")

    class Message(BaseModel):
        message:str = Field(..., description="Message")

    class Signature(BaseModel):
        signature:str = Field(..., description="Signature")

    class IsValid(BaseModel):
        is_valid:bool = Field(..., description="Is valid signature")