from typing import Optional, List
from fastapi import APIRouter, Body, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo import ReturnDocument

from app.database import getDB
from app.schemas import shopSchema as ss, bson
from app import oauth2

router = APIRouter(
    prefix = "/shops",
    tags = ["Shops"]
)


@router.get("/", response_model=List[ss.ShopModel], status_code=status.HTTP_200_OK , response_description="Get all shops")
async def getAllshops(db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Depends(oauth2.getCurrentUser)):
    shops = await db.shops.find().to_list(length=None)
    return shops

@router.get("/{id}", response_model=ss.ShopModel, status_code=status.HTTP_200_OK , response_description="Get Shops by Id")
async def getShopById(id: bson.PyObjectId, db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Depends(oauth2.getCurrentUser)):
    print(id, type(id))
    if (shop := await db.shops.find_one({"_id": id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shop with id {id} not found")
    return shop

@router.post("/", response_model=ss.ShopModel, status_code=status.HTTP_201_CREATED , response_description="Create a Shop")
async def createshop(shop: ss.ShopModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Depends(oauth2.getCurrentUser)):
    shop = jsonable_encoder(shop)
    shop["_id"] = bson.PyObjectId(shop["_id"])
    newShop = await db.shops.insert_one(shop)
    createdShop = await db.shops.find_one({"_id": newShop.inserted_id})
    return createdShop

@router.put("/{id}", response_model=ss.ShopModel, status_code=status.HTTP_200_OK, response_description="Update Shop")
async def updateShopById(id: bson.PyObjectId, shop: ss.UpdateShopModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Depends(oauth2.getCurrentUser)):
    shop = {k:v for k,v in shop.dict().items() if v is not None}
    shop["owner"] = {k: v for k, v in shop["owner"].items() if v is not None}
    for k,v in shop["owner"].items():
        print(k,v)
        shop[f"owner.{k}"] = v  
    shop.pop("owner")
    updatedShop = await db.shops.find_one_and_update({"_id": id}, {"$set": {**shop}}, return_document=ReturnDocument.AFTER)    
    if not updatedShop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shop with id {id} not found")
    return updatedShop

@router.delete("/{id}", response_model=ss.ShopModel, status_code=status.HTTP_200_OK, response_description="Delete Shop")
async def deleteShopById(id: bson.PyObjectId, db: AsyncIOMotorDatabase=Depends(getDB), currentUser: int = Depends(oauth2.getCurrentUser)):
    deletedShop = await db.shops.find_one_and_delete({"_id": id})    
    if not deletedShop:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shop with id {id} not found")
    return deletedShop