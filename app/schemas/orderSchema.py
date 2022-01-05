from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ValidationError
from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.schemas.bsonUtil import PyObjectId
from app.schemas.shopSchema import ShopBaseModel
from app.schemas.userSchema import UserBaseModel
from app.schemas.productSchema import ProductResponseModel

# from bsonUtil import PyObjectId
# from shopSchema import ShopModel
# from userSchema import UserResponseModel

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
    product: ProductResponseModel = Field(...)
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
                "item": "Surf Excel 1kg",
                "pprice": 200,
                "qty": 5,
                "gst": 36,
                "total": 236
            }
        }

class OrderBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    shop: ShopBaseModel = Field(...)
    status: OrderStatus = Field(...)
    items: List[OrderItemModel] = Field(...)
    billAmt: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra = {
            "example": {
                "shop": {"addr": "Shop# 5, Anaj Mandi",
                            "location": "Anaj Mandi",
                            "city": "Sonepat",
                            "state": "Haryana",
                            "owner":{
                                "name": "Chetan",
                                "TAN": "ARBIT789TAN999",
                                "phone": 9876543210,
                                "email": "chetan@shop.com",
                            }
                        },
                "status": "notProcessed",
                "items": [
                    {"item": "Surf Excel 1kg",
                     "pprice": 200,
                     "qty": 5,
                     "gst": 36,
                     "total": 236
                    },
                    {"item": "Tata Tea 1Kg",
                     "pprice": 120,
                     "qty": 2,
                     "gst": 21.6,
                     "total": 141.6
                    },
                ],
                "billAmt": 377.6
            }
        }

class OrderResponseModel(OrderBaseModel):
    createdAt: datetime = Field(...)
    lastUpdatedAt: datetime = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}


class BillModel(OrderBaseModel):
    customer: UserBaseModel = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra = {
            "example": {
                "shop": {"addr": "Shop# 5, Anaj Mandi",
                            "location": "Anaj Mandi",
                            "city": "Sonepat",
                            "state": "Haryana",
                            "owner":{
                                "name": "Chetan",
                                "TAN": "ARBIT789TAN999",
                                "phone": 9876543210,
                                "email": "chetan@shop.com",
                            }
                        },
                "status": "notProcessed",
                "items": [
                    {"item": "Surf Excel 1kg",
                     "pprice": 200,
                     "qty": 5,
                     "gst": 36,
                     "total": 236
                    },
                    {"item": "Tata Tea 1Kg",
                     "pprice": 120,
                     "qty": 2,
                     "gst": 21.6,
                     "total": 141.6
                    },
                ],
                "billAmt": 377.6
            }
        }

if __name__ == "__main__":
    print(BillModel.schema_json(indent=5))