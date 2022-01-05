from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ValidationError
from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.schemas.bsonUtil import PyObjectId
from app.schemas.shopSchema import ShopBaseModel
from app.schemas.userSchema import UserResponseModel

# from bsonUtil import PyObjectId
# from shopSchema import ShopModel
# from userSchema import UserResponseModel

class ProductStatus(str, Enum):
    active = "active"
    discontinued = "discontinued"

class CatalogBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    category: str = Field(...)
    ctgPath: str = Field(...)
    parents: List[str] = Field(...)
    children: List[str] = Field(...)
    isLeaf: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}

class ProductBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    productName: str = Field(...)
    ctgname : str = Field(...)
    category : str = Field(...)
    pprice: float = Field(...)
    sprice: float = Field(...)
    discount: float = Field(...)
    avlQty: float = Field(...)
    status: ProductStatus = Field(...)
    shop: ShopBaseModel = Field(...)
    

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra = {
            "example": {
            }
        }

class ProductResponseModel(ProductBaseModel):
    createdAt: datetime = Field(...)
    lastUpdatedAt: datetime = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra = {
            "example": {
            }
        }

class ProductUpdateModel(BaseModel):
    productName: Optional[str] 
    ctgname : Optional[str] 
    category : Optional[str] 
    pprice: Optional[float] 
    sprice: Optional[float]
    discount: Optional[float]
    avlQty: Optional[float] 
    status: Optional[ProductStatus] 
    shop: Optional[ShopBaseModel] 
    

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
            }
        }


if __name__ == "__main__":
    print(ProductBaseModel.schema_json(indent=5))