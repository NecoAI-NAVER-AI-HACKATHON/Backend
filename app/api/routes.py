from fastapi import APIRouter

from app.api.endpoints.health import router as health_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.user import router as user_router
from app.api.endpoints.workspace import router as workspace_router
from app.api.endpoints.system import router as system_router
from app.api.endpoints.system_execution import router as system_execution_router

routers = APIRouter()
router_list = [
    health_router,
    auth_router,
    user_router,
    workspace_router,
    system_router,
    system_execution_router,
]

for router in router_list:
    router.tags = routers
    routers.include_router(router)
