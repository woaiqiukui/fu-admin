from typing import List
from ninja import Router, ModelSchema, Query, Field
from ninja.pagination import paginate

from task.models import Project
from utils.fu_crud import create, delete, update, retrieve, ImportSchema, export_data, import_data
from utils.fu_ninja import FuFilters, MyPagination

router = Router()

# 设置过滤字段
class Filters(FuFilters):
    name: str = Field(None, alias="project_name")
    desc: str = Field(None, alias="project_desc")
    status: int = Field(None, alias="project_status")
    id: str = Field(None, alias="project_id")

# 设置请求接收字段
class ProjectSchemaIn(ModelSchema):
    class Config:
        model = Project
        model_fields = ['project_name', 'project_desc', 'project_status']


# 设置响应字段
class ProjectSchemaOut(ModelSchema):
    class Config:
        model = Project
        model_fields = "__all__"

# 创建Project
@router.post("/project", response=ProjectSchemaOut)
def create_demo(request, data: ProjectSchemaIn):
    project = create(request, data, Project)
    return project

# 删除Project
@router.delete("/project/{project_id}")
def delete_demo(request, project_id: int):
    delete(project_id, Project)
    return {"success": True}


# 更新Project
@router.put("/project/{project_id}", response=ProjectSchemaOut)
def update_demo(request, project_id: int, data: ProjectSchemaIn):
    project = update(request, project_id, data, Project)
    return project

# 获取Project List
@router.get("/project", response=List[ProjectSchemaOut])
@paginate(MyPagination)
def get_demo_list(request, filters: Filters = Query(...)):
    return retrieve(request, Project, filters)


