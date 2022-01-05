from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.schemas.bsonUtil import PyObjectId
from app.schemas.userSchema import UserResponseModel
from app.schemas.productSchema import ProductResponseModel, ProductStatus

# from bsonUtil import PyObjectId
# from shopSchema import ShopModel
# from userSchema import UserResponseModel

class CartItemModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    product: ProductResponseModel = Field(...)
    price: float = Field(...)
    qty: float = Field(...)
    gst: float = Field(...)
    total: float = Field(...)

class CartBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    customer: UserResponseModel = Field(...)
    items: List[CartItemModel] = Field(...)
    

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}

class CartResponseModel(CartBaseModel):
    createdAt: datetime = Field(...)
    lastUpdatedAt: datetime = Field(...)
    

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}


class CartUpdateModel(BaseModel):
    cartItemId: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    qty: Optional[int] 
    status: Optional[ProductStatus] 

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
            }
        }


if __name__ == "__main__":
    print(CartBaseModel.schema_json(indent=5))