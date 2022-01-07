from typing import Optional, List
from fastapi import APIRouter, Body, status, Security
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo import ReturnDocument

from app.database import getDB
from app.schemas import postSchema as ps, bsonUtil as bson, userSchema as us
from app import oauth2

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)


@router.get("/", response_model=List[ps.PostModel], status_code=status.HTTP_200_OK , response_description="Get all posts")
# async def getAllPosts(db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Depends(oauth2_1.getCurrentUser)):
async def getAllPosts(db: AsyncIOMotorDatabase = Depends(getDB), currentUser: us.UserCreateModel = Security(oauth2.getCurrentUser, scopes=["admin"])):
    print(currentUser)
    posts = await db.posts.find().to_list(length=None)
    return posts

@router.get("/{id}", response_model=ps.PostModel, status_code=status.HTTP_200_OK , response_description="Get posts by Id")
async def getPostById(id: bson.PyObjectId, db: AsyncIOMotorDatabase = Depends(getDB)):
    if (post := await db.posts.find_one({"_id": id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post

@router.post("/", response_model=ps.PostModel, status_code=status.HTTP_201_CREATED , response_description="Create a post")
async def createPost(post: ps.PostModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB)):
    post = jsonable_encoder(post)
    print(post)
    newPost = await db.posts.insert_one(post)
    createdPost = await db.posts.find_one({"_id": newPost.inserted_id})
    return createdPost

@router.put("/{id}", response_model=ps.PostModel, status_code=status.HTTP_200_OK, response_description="Update Post")
async def updatePostById(id: bson.PyObjectId, post: ps.UpdatePostModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB)):
    postDict = post.dict()
    updatedPost = await db.posts.find_one_and_update({"_id": id}, {"$set": {**postDict}}, return_document=ReturnDocument.AFTER)    
    if not updatedPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

@router.delete("/{id}", response_model=ps.PostModel, status_code=status.HTTP_200_OK, response_description="Update Post")
async def deletePostById(id: bson.PyObjectId, db: AsyncIOMotorDatabase=Depends(getDB)):
    deletedPost = await db.posts.find_one_and_delete({"_id": id})    
    if not deletedPost:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return deletedPost