from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from app.schemas.bson import PyObjectId
from datetime import datetime

class UserBase(BaseModel):
    id: EmailStr = Field(default_factory=EmailStr, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
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
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "john.doe@example.com",
                "createdAt": "2022-01-03T01:29:51.747000",
            }
        }

class UserCreateModel(UserBase):
    password: str = Field(...)
    type: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "john.doe@example.com",
                "password":"notagoodpassword",
            }
        }

