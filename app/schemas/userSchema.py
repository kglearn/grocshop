from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ValidationError
from datetime import datetime
from enum import Enum

class UserType(str, Enum):
    admin = "admin"
    customer = "customer"
    shopOwner = "shopOwner"
    shopAdmin = "shopAdmin"


class UserBase(BaseModel):
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


class UserResponseModel(UserBase):
    createdAt: datetime  = Field(...)

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "_id": "john.doe@example.com",
                "createdAt": "2022-01-03T01:29:51.747000",
            }
        }

class UserCreateModel(UserBase):
    password: str = Field(...)
    type: UserType = Field(...)
    

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "_id": "john.doe@example.com",
                "password":"notagoodpassword",
            }
        }


if __name__ == "__main__":
    print(UserCreateModel.schema_json(indent=2))