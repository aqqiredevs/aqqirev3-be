from fastapi import APIRouter
from app.controllers import property_router, user_router

router = APIRouter(prefix="/api")

router.include_router(property_router)
router.include_router(user_router)
