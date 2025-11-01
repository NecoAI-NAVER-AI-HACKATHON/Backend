from fastapi import APIRouter

from app.api.endpoints.health import router as health_router
from app.api.endpoints.auth import router as auth_router

routers = APIRouter()
router_list = [health_router, auth_router]

for router in router_list:
    router.tags = routers
    routers.include_router(router)
