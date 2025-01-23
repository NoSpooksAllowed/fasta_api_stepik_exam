from fastapi import FastAPI
from app.routers import category
from app.routers import products
from app.routers import auth
from app.routers import permission
from app.routers import reviews

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(permission.router)
app.include_router(reviews.router)