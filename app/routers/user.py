from typing import Optional, List
from fastapi import APIRouter, Body, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from datetime import datetime

from app.database import getDB
from app.schemas import userSchema as us
from app import utils, oauth2

router = APIRouter(
    prefix = "/users",
    tags = ["End Users"]
)


@router.get("/", response_model=List[us.UserResponseModel], status_code=status.HTTP_200_OK , response_description="Get all users")
async def getAllUsers(db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Depends(oauth2.getCurrentUser)):
    print(currentUser)
    if currentUser["type"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not permitted for this operation")
    users = await db.users.find().to_list(length=None)
    return users

@router.get("/{id}", response_model=us.UserResponseModel, status_code=status.HTTP_200_OK , response_description="Get Users by Id")
async def getUserById(id: str, db: AsyncIOMotorDatabase = Depends(getDB)):
    if (user := await db.users.find_one({"_id": id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

@router.post("/", response_model=us.UserResponseModel, status_code=status.HTTP_201_CREATED , response_description="Create a User")
async def createUser(user: us.UserCreateModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB)):
    user = jsonable_encoder(user)
    user["createdAt"] = datetime.now()
    user["password"] = utils.hashPasswd(user["password"])
    try:
        newUser = await db.users.insert_one(user)
    except DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email address - {user['_id']} - already exists")

    createdUser = await db.users.find_one({"_id": newUser.inserted_id})
    return createdUser

@router.put("/{id}", response_model=us.UserResponseModel, status_code=status.HTTP_200_OK, response_description="Update User")
async def updateUserById(user: us.UserCreateModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB)):
    print(user.dict())
    updatedUser = await db.users.find_one_and_update({"_id": user.id}, {"$set": {"password": user.password}}, return_document=ReturnDocument.AFTER)    
    if not updatedUser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return updatedUser

@router.delete("/{id}", response_model=us.UserResponseModel, status_code=status.HTTP_200_OK, response_description="Update User")
async def deleteUserById(id: str, db: AsyncIOMotorDatabase = Depends(getDB)):
    deletedUser = await db.users.find_one_and_delete({"_id": id})    
    if not deletedUser:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return deletedUser