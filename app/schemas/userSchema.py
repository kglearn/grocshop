from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from enum import Enum


class UserType(str, Enum):
    admin = "admin"
    customer = "customer"
    shopOwner = "shopOwner"
    shopAdmin = "shopAdmin"

# Base Model. Also used for creation
class UserBaseModel(BaseModel):
    id: EmailStr = Field(default_factory=EmailStr, alias="_id")
    addr: str = Field(...)
    city: str = Field(...)
    location: str = Field(...)
    state: str = Field(...)
    phone: int = Field(...)
    

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "id": "john.doe@example.com",
                "location": "Mandi Area",
            }
        }

class UserResponseModel(UserBaseModel):
    orderHistory: Optional[List[OrderResponseModel]] = None
    createdAt: datetime  = Field(...)
    lastUpdatedAt: datetime = Field(...)

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "_id": "a@b.c",
                "addr": "some addr",
                "city": "city1",
                "location": "Block1",
                "state": "state1",
                "phone": 1234567890,
                "createdAt": "2022-01-04T11:59:02.666000"
            }
        }

class UserCreateModel(UserBaseModel):
    password: str = Field(...)
    type: UserType = Field(...)
    

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "id": "a@b.c",
                "password":"abc",
                "addr": "some addr",
                "city": "city1",
                "location": "BlockA",
                "state": "state1",
                "phone": 1234567890,
                "type": "admin"
            }
        }


class UserUpdateModel(UserBaseModel):
    addr: Optional[str] 
    city: Optional[str] 
    location: Optional[str] 
    state: Optional[str]
    phone: Optional[int]
    password: Optional[str]
    type: Optional[UserType]
    
    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "id": "a@b.c",
                "location": "Block1",
                "password":"abc",
                "type": "shopOwner"
            }
        }


from app.schemas.orderSchema import OrderResponseModel
UserBaseModel.update_forward_refs()
UserResponseModel.update_forward_refs()

if __name__ == "__main__":
    print(UserCreateModel.schema_json(indent=2))