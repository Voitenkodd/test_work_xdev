from fastapi import APIRouter

from api.basket import router as basket
from api.mushroom import router as mushroom

api_router = APIRouter(prefix="/api")
api_router.include_router(mushroom, tags=["mushroom"])
api_router.include_router(basket, tags=["basket"])
