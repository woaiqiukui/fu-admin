from ninja import Router
from .apis.new_task import router

task_router = Router()
task_router.add_router('/new_task', router, tags=["new_task"])
