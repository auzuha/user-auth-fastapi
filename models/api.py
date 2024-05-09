from pydantic import BaseModel
from typing import List, Optional, Dict
from models.models import User, UserFilter
import uuid

#tokens request and response
class GetTokenRequest(BaseModel):
    userId: str

class GetTokenResponse(BaseModel):
    token: str

#users request and response
class GetUsersRequest(BaseModel):
    filter: Optional[UserFilter]

class GetUsersResponse(BaseModel):
    results: List[User]


class CreateUserRequest(BaseModel):
    userId: Optional[str] = str(uuid.uuid4())
    username: str
    firstName: str
    lastName: str
    metadata: Optional[Dict] = None


class UpdateUserRequest(BaseModel):
    update: Dict

class UpdateUserResponse(BaseModel):
    success: bool