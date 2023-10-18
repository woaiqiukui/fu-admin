from ninja import Router
from .apis.project import router as project_router

task_router = Router()
task_router.add_router('/', project_router, tags=["project"])
