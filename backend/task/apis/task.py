from typing import List
import uuid
from ninja import Router, ModelSchema, Query, Field
from ninja.pagination import paginate
from utils.yunying_crud import create, delete, update, retrieve, ImportSchema, export_data, import_data
from utils.fu_ninja import YunYingFilters, MyPagination
from ..models import Task


router = Router()

# 设置过滤字段
class Filters(YunYingFilters):
    task_name: str = Field(None, alias="task_name")
    project_uuid: uuid.UUID = Field(None, alias="project_uuid")
    task_desc: str = Field(None, alias="task_desc")
    task_type: str = Field(None, alias="task_type")
    task_status: str = Field(None, alias="task_status")
    task_uuid: str = Field(None, alias="task_uuid")

# 设置请求接收字段
class TaskSchemaIn(ModelSchema):
    class Config:
        model = Task
        model_fields = "__all__"

# 删除 Task
@router.delete("/{task_uuid}")
def delete_task(request, task_uuid: uuid.UUID):
    delete(task_uuid, Task)
    return {"success": True}

# 更新 Task
@router.put("/{task_uuid}", response=TaskSchemaIn)
def update_task(request, task_uuid: uuid.UUID, data: TaskSchemaIn):
    task = update(request, task_uuid, data, Task)
    return task

# 获取 Task List
@router.get("/", response=List[TaskSchemaIn])
@paginate(MyPagination)
def get_task_list(request, filters: Filters = Query(...)):
    return retrieve(request, Task, filters)

# 暂停 Task
@router.post("/pause/{task_uuid}", response=TaskSchemaIn)
def pause_task(request, task_uuid: uuid.UUID):
    task = Task.objects.get(uuid=task_uuid)
    task.task_status = '2'
    task.save()
    return task

# 恢复 Task
@router.post("/resume/{task_uuid}", response=TaskSchemaIn)
def resume_task(request, task_uuid: uuid.UUID):
    task = Task.objects.get(uuid=task_uuid)
    task.task_status = '1'
    task.save()
    return task