from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic.error_wrappers import ValidationError

from app.schemas import tokenSchema
from app.config import settings
from app.database import getDB
from app.utils import intersection

oauth2Scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes = {"admin": "System wide Access of all endpoints", 
              "shopOwner": "Access of all shop endpoints", 
              "shopAdmin": "Admin access of shop endpoints",
              "customer": "Access of only consumer endpoints",
              }
    )

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

        tokenScopes = payload.get("scopes", [])     
        tokenData = tokenSchema.TokenData(scopes=tokenScopes, id=id)

    except (JWTError, ValidationError) as e:
        print(e)
        raise credentials_exception
    
    return tokenData

async def getCurrentUser(securityScope: SecurityScopes, token: str = Depends(oauth2Scheme), db: AsyncIOMotorDatabase=Depends(getDB)):

    if securityScope.scopes:
        authenticate_value = f'Bearer scope="{securityScope.scope_str}"'
    else:
        authenticate_value = f"Bearer"
        credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": authenticate_value},
    )
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    tokenData = await verifyAccessToken(token, credentials_exception)

    if (user := await db.users.find_one({"_id": tokenData.id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {token.id} not found")

    if not intersection(securityScope.scopes, tokenData.scopes):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission denied")

    return user