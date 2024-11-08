from fastapi import APIRouter

from app.api.API_v1.Endpoints import User
from app.api.API_v1.Endpoints import Document
from app.api.API_v1.Endpoints import Permission



# Initialize API router
api_router = APIRouter()

# Routers
api_router.include_router(User.router, prefix="/User", tags=["User"])
api_router.include_router(Document.router, prefix="/Document", tags=["Document"])
api_router.include_router(Permission.router, prefix="/Permission", tags=["Permission"])
