from fastapi import FastAPI
from app.database import getDB
from app.routers import user, auth, shop, product, post, cart

app = FastAPI()

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(shop.router)
app.include_router(product.router)
app.include_router(cart.router)


