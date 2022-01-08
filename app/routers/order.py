from typing import Optional, List
from fastapi import APIRouter, Body, status, Security
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo import ReturnDocument
from datetime import datetime

from app.database import getDB
from app.schemas import orderSchema as ors, bsonUtil as bson
from app import oauth2

router = APIRouter(
    prefix = "/orders",
    tags = ["Orders"]
)


@router.get("/", response_model=List[ors.OrderResponseModel], status_code=status.HTTP_200_OK , response_description="Get all Orders")
async def getAllOrders(db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin"])):
    orders = await db.orders.find().to_list(length=None)
    return orders

@router.get("/{id}", response_model=ors.OrderResponseModel, status_code=status.HTTP_200_OK , response_description="Get Order by Id")
async def getOrderById(id: bson.PyObjectId, db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    print(id, type(id))
    if (order := await db.orders.find_one({"_id": id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")
    print(order)
    return order

@router.post("/", response_model=ors.OrderResponseModel, status_code=status.HTTP_201_CREATED , response_description="Create an Order")
async def createOrder(order: ors.OrderBaseModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    order = jsonable_encoder(order)
    order["_id"] = bson.PyObjectId(order["_id"])
    # The shop, items information would  be cached in the application / fetched from DB at the time of creation of order. 
    # therefore, the below lines are subject to change
    order["shop"]["_id"] = bson.PyObjectId(order["shop"]["_id"]) 
    for idx, item in enumerate(order["items"]):
        order["items"][idx]["_id"] = bson.PyObjectId(item["_id"])
    order["createdAt"] = datetime.now()
    order["lastUpdatedAt"] = datetime.now()

    newOrder = await db.orders.insert_one(order)
    print(newOrder.inserted_id)
    createdOrder = await db.orders.find_one({"_id": newOrder.inserted_id})
    print(createdOrder)
    return createdOrder

@router.put("/updateDiscount/{id}", response_model=ors.OrderResponseModel, status_code=status.HTTP_200_OK, response_description="Update Order")
async def updateOrderDiscountById(id: bson.PyObjectId, orderUpdate: List[ors.OrderUpdateDiscountModel] = Body(...), db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    for item in orderUpdate:
        print(item)
        updatedOrder = await db.orders.update_one({"_id": id, "items._id": item.productId}, {"$set":{"items.$.discount": item.discount}})
    
    updatedOrder = await db.orders.find_one({"_id": id})
    return updatedOrder

@router.put("/updateStatus/{id}", response_model=ors.OrderResponseModel, status_code=status.HTTP_200_OK, response_description="Update Order")
async def updateOrderStatusById(id: bson.PyObjectId, orderUpdate: ors.OrderUpdateStatusModel = Body(...), db: AsyncIOMotorDatabase = Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin", "shopOwner", "shopAdmin"])):
    updatedOrder = await db.orders.update_one({"_id": id}, {"$set":{"status": orderUpdate.status}})
    
    updatedOrder = await db.orders.find_one({"_id": id})
    return updatedOrder

@router.delete("/{id}", response_model=ors.OrderResponseModel, status_code=status.HTTP_200_OK, response_description="Delete Order")
async def deleteOrderById(id: bson.PyObjectId, db: AsyncIOMotorDatabase=Depends(getDB), currentUser: int = Security(oauth2.getCurrentUser, scopes=["admin"])):
    deletedOrder = await db.orders.find_one_and_delete({"_id": id})    
    if not deletedOrder:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")
    return deletedOrder