from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    token: str
    tokenType: str

class TokenData(BaseModel):
    id: Optional[EmailStr] = None