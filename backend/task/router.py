from ninja import Router
from .apis.new_task import router as newtaskRouter
from .apis.task import router as taskRouter

task_router = Router()
task_router.add_router('/task', taskRouter, tags=["task"])
task_router.add_router('/new_task', newtaskRouter, tags=["new_task"])
