from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class User(BaseModel):
    userId: str
    username: str
    firstName: str
    lastName: str
    metadata: Optional[Dict] = None
