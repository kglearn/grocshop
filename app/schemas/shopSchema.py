from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from app.schemas.bsonUtil import PyObjectId


class OwnerModel(BaseModel):
    name: str = Field(...)
    TAN: str = Field(...)
    phone: int = Field(...)
    email: EmailStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra = {
            "example": {
                "name": "Chetan",
                "TAN": "ARBIT789TAN999",
                "phone": 9876543210,
                "email": "chetan@shop.com",
            }
        }

class UpdateOwnerModel(BaseModel):
    name: Optional[str] 
    TAN: Optional[str]
    phone: Optional[int]
    email: Optional[EmailStr] 

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra = {
            "example": {
                "name": "Chetan",
                "TAN": "ARBIT789TAN999",
                "phone": 9876543210,
                "email": "chetan@shop.com",
            }
        }


class ShopModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    addr: str = Field(...)
    location: str = Field(...)
    city: str = Field(...)
    state: str = Field(...) 
    owner: OwnerModel = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra = {
            "example": {
                "addr": "Shop# 5, Anaj Mandi",
                "location": "Anaj Mandi",
                "city": "Sonepat",
                "state": "Haryana",
                "owner":{
                    "name": "Chetan",
                    "TAN": "ARBIT789TAN999",
                    "phone": 9876543210,
                    "email": "chetan@shop.com",
                }
            }
        }


class UpdateShopModel(BaseModel):
    addr: Optional[str] 
    location: Optional[str] 
    city: Optional[str] 
    state: Optional[str]
    owner: Optional[UpdateOwnerModel] 

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "addr": "Shop# 5, Anaj Mandi",
                "location": "Anaj Mandi",
                "city": "Sonepat",
                "state": "Haryana",
                "owner":{
                    "name": "Chetan",
                    "TAN": "ARBIT789TAN999",
                    "phone": 9876543210,
                    "email": "chetan@shop.com",
                }
            }
        }

