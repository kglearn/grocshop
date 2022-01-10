import motor.motor_asyncio
from app.config import settings
import traceback

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(f"{settings.database_uri}")
except Exception as e:
    print(e)


def getDB():
    db = client[settings.database_name]
    try:
        yield db
    except Exception as e:
        print(e)
        traceback.print_exc()