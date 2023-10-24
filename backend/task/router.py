from ninja import Router
from .api import router

task_router = Router()
task_router.add_router('/', router, tags=["task"])
