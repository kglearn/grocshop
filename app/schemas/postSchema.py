from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from app.schemas.bsonUtil import PyObjectId


class PostModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    content: str = Field(...)
    likes: Optional[int] 

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


class UpdatePostModel(BaseModel):
    title: Optional[str]
    content: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "post title",
                "content": "post content",
                "likes": 5,
            }
        }

