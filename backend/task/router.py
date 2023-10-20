from ninja import Router
from .apis.project import router as project_router
from .apis.public_assets import router as public_assets_router

task_router = Router()
task_router.add_router('/', project_router, tags=["project"])
task_router.add_router('/', public_assets_router, tags=["public_assets"])
