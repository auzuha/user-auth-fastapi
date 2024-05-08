from pydantic import BaseModel

class GetTokenRequest(BaseModel):
    userId: str

class GetTokenResponse(BaseModel):
    token: str