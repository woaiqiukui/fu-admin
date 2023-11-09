from typing import List
import uuid
from ninja import Router, ModelSchema, Query, Field
from ninja.pagination import paginate
from utils.yunying_crud import create, delete, update, retrieve, ImportSchema, export_data, import_data
from utils.fu_ninja import FuFilters, MyPagination

from .models import Task

router = Router()

# 设置过滤字段
class Filters(FuFilters):
    name: str = Field(None, alias="task_name")
    desc: str = Field(None, alias="task_desc")
    type: int = Field(None, alias="task_type")
    task_uuid: str = Field(None, alias="task_uuid")
    status: str = Field(None, alias="task_status")

# 设置请求接收字段
class TaskSchemaIn(ModelSchema):
    class Config:
        model = Task
        model_fields = ['task_name', 'task_desc', 'task_type', 'task_status']


# 设置响应字段
class TaskSchemaOut(ModelSchema):
    class Config:
        model = Task
        model_fields = "__all__"

# 创建Task
@router.post("/", response=TaskSchemaOut)
def create_demo(request, data: TaskSchemaIn):
    task = create(request, data, Task)
    return task

# 删除Task
@router.delete("/{task_uuid}")
def delete_demo(request, task_uuid: uuid.UUID):
    delete(task_uuid, Task)
    return {"success": True}

# 更新Task
@router.put("/{task_uuid}", response=TaskSchemaOut)
def update_demo(request, task_uuid: uuid.UUID, data: TaskSchemaIn):
    task = update(request, task_uuid, data, Task)
    return task

# 获取Task List
@router.get("/", response=List[TaskSchemaOut])
@paginate(MyPagination)
def get_demo_list(request, filters: Filters = Query(...)):
    return retrieve(request, Task, filters)

