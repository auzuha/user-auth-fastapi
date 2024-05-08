from pydantic import BaseModel
from typing import Optional, Dict

class User(BaseModel):
    userId: str
    username: str
    firstName: str
    lastName: str
    metadata: Optional[Dict] = None

class UserFilter(BaseModel):
    userId: Optional[str] = None
    username: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    metadata: Optional[Dict] = None