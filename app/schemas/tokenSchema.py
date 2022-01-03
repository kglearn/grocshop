from typing import Optional, List
from pydantic import BaseModel, EmailStr, ValidationError


class Token(BaseModel):
    token: str
    tokenType: str

class TokenData(BaseModel):
    id: Optional[EmailStr] = None
    scopes: List[str] = []