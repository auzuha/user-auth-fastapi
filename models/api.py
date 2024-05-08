from pydantic import BaseModel
from typing import List, Optional
from models.models import User, UserFilter

class GetTokenRequest(BaseModel):
    userId: str

class GetTokenResponse(BaseModel):
    token: str

class GetUsersRequest(BaseModel):
    filter: Optional[UserFilter]

class GetUsersResponse(BaseModel):
    results: List[User]