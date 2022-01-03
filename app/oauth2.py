from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas import tokenSchema
from app.config import settings
from app.database import getDB

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_toke_expire_minutes

def createAccessToken(data: dict):
    dataCopy = data.copy()  
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dataCopy.update({"exp": expire})

    encodedJWT = jwt.encode(dataCopy, SECRET_KEY, algorithm=ALGORITHM)

    return encodedJWT

async def verifyAccessToken(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("userId")

        if id is None:
            raise credentials_exception

        tokenData = tokenSchema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return tokenData

async def getCurrentUser(token: str = Depends(oauth2Scheme), db: AsyncIOMotorDatabase=Depends(getDB)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials", headers={"WWW-Authenticate": "Bearer"})

    token = await verifyAccessToken(token, credentials_exception)

    if (user := await db.users.find_one({"_id": token.id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {token.id} not found")

    return user