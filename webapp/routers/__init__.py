from fastapi import APIRouter

from webapp.routers.talk import router as router_talk
from webapp.routers.web import router as router_web


router = APIRouter()

# API
router.include_router(router_talk, tags=["talk"], prefix="/api/talk")

# Web interface
router.include_router(router_web, tags=["web"], prefix="")
