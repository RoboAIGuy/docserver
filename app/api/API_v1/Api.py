from fastapi import APIRouter

# from app.api.API_v1.Endpoints import Users
from app.api.API_v1.Endpoints import Video




# Initialize API router
api_router = APIRouter()

# Routers
# api_router.include_router(Users.router, prefix="/products", tags=["Products"])
api_router.include_router(Video.router, prefix="/Video", tags=["Video"])
