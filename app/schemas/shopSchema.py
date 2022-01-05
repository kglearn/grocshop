from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from app.schemas.bsonUtil import PyObjectId
# from bsonUtil import PyObjectId

class OwnerModel(BaseModel):
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra = {
            "example": {
                "name": "Chetan"
            }
        }

class OwnerUpdateModel(BaseModel):
    name: Optional[str] 

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra = {
            "example": {
                "name": "Chetan"
            }
        }


class ShopBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    addr: str = Field(...)
    location: str = Field(...)
    city: str = Field(...)
    state: str = Field(...) 
    gstin: str = Field(...)
    phone: int = Field(...)
    email: EmailStr = Field(...)
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
                "gstin": "ARBIT789TAN999",
                "phone": 9876543210,
                "email": "chetan@shop.com",
                "owner":{
                    "name": "Chetan"
                }
            }
        }

class ShopResponseModel(ShopBaseModel):
    createdAt: datetime = Field(...)
    lastUpdatedAt: datetime = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}


class ShopUpdateModel(BaseModel):
    addr: Optional[str] 
    location: Optional[str] 
    city: Optional[str] 
    state: Optional[str]
    gstin: Optional[str]
    phone: Optional[int]
    email: Optional[EmailStr] 
    owner: Optional[OwnerUpdateModel] 

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "addr": "Shop# 5, Anaj Mandi",
                "location": "Anaj Mandi",
                "city": "Sonepat",
                "state": "Haryana",
                "gstin": "ARBIT789TAN999",
                "phone": 9876543210,
                "email": "chetan@shop.com",
                "owner":{
                    "name": "Chetan"
                }
            }
        }

# if __name__ == "__main__":
#     print(ShopModel.schema_json(indent=5))