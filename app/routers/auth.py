from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, SecurityScopes
from motor.motor_asyncio import AsyncIOMotorDatabase

from app import schemas, utils, oauth2
from app.database import getDB
from app.schemas import tokenSchema

router = APIRouter(
    tags = ["Authentication"]
)

@router.post("/login", response_model=tokenSchema.Token)
async def login(userCreds: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorDatabase = Depends(getDB)):

    if (user := await db.users.find_one({"_id": userCreds.username})) is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with emailId - {userCreds.username} - not found")

    if not utils.verifyPasswd(userCreds.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials p")

    print(user)
    token = oauth2.createAccessToken(data = {"userId": user["_id"]})
    print(token)
    return {"token": token, "tokenType": "bearer"}