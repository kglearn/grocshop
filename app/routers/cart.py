from typing import Optional, List
from fastapi import APIRouter, Body, status, Security
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo import ReturnDocument
from datetime import datetime

from app.database import getDB
from app.schemas import cartSchema as cs, bsonUtil as bson
from app import oauth2

router = APIRouter(
    prefix = "/carts",
    tags = ["Carts"]
)


@router.get("/", response_model=List[cs.CartResponseModel], status_code=status.HTTP_200_OK , response_description="Get all Carts")
# async def getAllshops(db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Depends(oauth2.getCurrentUser)):
async def getAllCarts(db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    carts = await db.carts.find().to_list(length=None)
    return carts

@router.get("/{id}", response_model=cs.CartResponseModel, status_code=status.HTTP_200_OK , response_description="Get Cart by Id")
async def getCartById(id: bson.PyObjectId, db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    if (cart := await db.carts.find_one({"_id": id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cart with id {id} not found")
    return cart

@router.post("/", response_model=cs.CartResponseModel, status_code=status.HTTP_201_CREATED , response_description="Create a Cart")
async def createCart(cart: cs.CartBaseModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    print("1 ->>> ", cart)
    cart = jsonable_encoder(cart)
    print("2 ->>> ", cart)
    cart["_id"] = bson.PyObjectId(cart["_id"])
    print("3 ->>", cart["items"])
    for idx, item in enumerate(cart["items"]):
        cart["items"][idx]["_id"] = bson.PyObjectId(item["_id"])
    cart["createdAt"] = datetime.now()
    cart["lastUpdatedAt"] = datetime.now()

    print(cart)

    newCart = await db.carts.insert_one(cart)
    createdCart = await db.carts.find_one({"_id": newCart.inserted_id})
    return createdCart

@router.put("/update/{id}", response_model=cs.CartResponseModel, status_code=status.HTTP_200_OK, response_description="Update Cart qty")
async def updateCartItemsById(id: bson.PyObjectId, cartUpdate: List[cs.CartItemUpdateModel] = Body(...), db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    for items in cartUpdate:
        updatedCart = await db.carts.update_one({"_id": id, "items._id": items.cartItemId}, {"$set":{"items.$.qty": items.qty}})
    
    updatedCart = await db.carts.find_one({"_id": id})
    return updatedCart

        
@router.put("/delete/{id}", response_model=cs.CartResponseModel, status_code=status.HTTP_200_OK, response_description="Delete Cart Items")
async def deleteCartItemsById(id: bson.PyObjectId, cartDelete: cs.CartItemDeleteModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    for itemId in cartDelete.cartItemId:
        deletedCart = await db.carts.update_one({"_id": id}, {"$pull":{"items": {"_id": itemId} }})

    deletedCart = await db.carts.find_one({"_id": id})
    return deletedCart

@router.delete("/{id}", response_model=cs.CartResponseModel, status_code=status.HTTP_200_OK, response_description="Delete Cart")
async def deleteCartById(id: bson.PyObjectId, db: AsyncIOMotorDatabase=Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin"])):
    deletedCart = await db.carts.find_one_and_delete({"_id": id})    
    if not deletedCart:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cart with id {id} not found")
    return deletedCart