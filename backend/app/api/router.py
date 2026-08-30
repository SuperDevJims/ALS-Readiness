from fastapi import APIRouter

from .routes import admin, auth, users

router = APIRouter(prefix="/api")

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(admin.router)
