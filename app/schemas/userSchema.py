from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ValidationError
from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.schemas.bsonUtil import PyObjectId

class UserType(str, Enum):
    admin = "admin"
    customer = "customer"
    shopOwner = "shopOwner"
    shopAdmin = "shopAdmin"


class UserBase(BaseModel):
    id: EmailStr = Field(default_factory=EmailStr, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "_id": "61d1bf9669654465394034fa",
                "email": "john.doe@example.com",
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