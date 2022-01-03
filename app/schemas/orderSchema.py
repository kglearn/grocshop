from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ValidationError
from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.schemas.bsonUtil import PyObjectId
from app.schemas.shopSchema import ShopModel



class OrderStatus(str, Enum):
    notProcessed = "notProcessed"
    inProcess = "inProcess"
    processed = "processed"
    shipped = "shipped"
    delivered = "delivered"
    waitForDelivery = "waitForDelivery"
    cxCancelled = "cxCancelled"
    spCancelled = "spCancelled"


class OrderItemModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    item: str = Field(...)
    pprice: float = Field(...)
    qty: float = Field(...)
    gst: float = Field(...)
    total: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra = {
            "example": {
                "title": "post title",
                "content": "post content",
                "likes": 5,
            }
        }


class OrderBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    shop: ShopModel = Field(...)
    status: OrderStatus = Field(...)
    items: List[OrderItemModel]
    billAmt: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra = {
            "example": {
                "title": "post title",
                "content": "post content",
                "likes": 5,
            }
        }