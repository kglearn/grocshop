from typing import Optional, List
from fastapi import APIRouter, Body, status, Security
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo import ReturnDocument
from datetime import datetime

from app.database import getDB
from app.schemas import productSchema as ps, bsonUtil as bson
from app import oauth2

router = APIRouter(
    prefix = "/products",
    tags = ["Products"]
)


@router.get("/", response_model=List[ps.ProductResponseModel], status_code=status.HTTP_200_OK , response_description="Get all Products")
# async def getAllshops(db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Depends(oauth2.getCurrentUser)):
async def getAllProducts(db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    products = await db.products.find().to_list(length=None)
    return products

@router.get("/{id}", response_model=ps.ProductResponseModel, status_code=status.HTTP_200_OK , response_description="Get Product by Id")
async def getProductById(id: bson.PyObjectId, db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    print(id, type(id))
    if (product := await db.products.find_one({"_id": id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    print(product)
    return product

@router.post("/", response_model=ps.ProductResponseModel, status_code=status.HTTP_201_CREATED , response_description="Create a Product")
async def createProduct(product: ps.ProductBaseModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    product = jsonable_encoder(product)
    product["_id"] = bson.PyObjectId(product["_id"])
    product["createdAt"] = datetime.now()
    product["lastUpdatedAt"] = datetime.now()

    newProduct = await db.products.insert_one(product)
    print(newProduct.inserted_id)
    createdProduct = await db.products.find_one({"_id": newProduct.inserted_id})
    print(createdProduct)
    return createdProduct

@router.put("/{id}", response_model=ps.ProductResponseModel, status_code=status.HTTP_200_OK, response_description="Update Product")
async def updateProductById(id: bson.PyObjectId, product: ps.ProductUpdateModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    product = {k:v for k,v in product.dict().items() if v is not None}
    if "shop" in product.keys():
        product["shop"] = {k: v for k, v in product["shop"].items() if v is not None}

        for k,v in product["shop"].items():
            product[f"shop.{k}"] = v  

        if "owner" in product["shop"].keys():
            for k,v in product["shop"]["owner"].items():
                product[f"shop.owner.{k}"] = v  
            product.pop("shop.owner")
        product.pop("shop")

    product["lastUpdatedAt"] = datetime.now()
    
    updatedProduct = await db.products.find_one_and_update({"_id": id}, {"$set": {**product}}, return_document=ReturnDocument.AFTER)    
    if not updatedProduct:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    return updatedProduct

@router.delete("/{id}", response_model=ps.ProductResponseModel, status_code=status.HTTP_200_OK, response_description="Delete Product")
async def deleteProductById(id: bson.PyObjectId, db: AsyncIOMotorDatabase=Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin"])):
    deletedProduct = await db.products.find_one_and_delete({"_id": id})    
    if not deletedProduct:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    return deletedProduct