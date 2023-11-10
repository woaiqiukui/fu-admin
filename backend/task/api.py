from typing import List
import uuid
from ninja import Router, ModelSchema, Query, Field
from ninja.pagination import paginate
from project.models import Project
from utils.yunying_crud import create, delete, update, retrieve, ImportSchema, export_data, import_data
from utils.fu_ninja import YunYingFilters, MyPagination

from .models import Task

router = Router()

# 设置过滤字段
class Filters(YunYingFilters):
    task_name: str = Field(None, alias="task_name")
    project_uuid: uuid.UUID = Field(None, alias="project_uuid")
    task_desc: str = Field(None, alias="task_desc")
    task_type: str = Field(None, alias="task_type")
    task_status: str = Field(None, alias="task_status")
    full_company_name_input: str = Field(None, alias="full_company_name_input")
    root_domain_input: str = Field(None, alias="root_domain_input")
    ip_input: str = Field(None, alias="ip_input")
    domain_brute_force: bool = Field(None, alias="domain_brute_force")
    historical_domain_query: bool = Field(None, alias="historical_domain_query")
    port_scanning: bool = Field(None, alias="port_scanning")
    framework_identification: bool = Field(None, alias="framework_identification")
    fingerprint_identification: bool = Field(None, alias="fingerprint_identification")
    fofa: bool = Field(None, alias="fofa")
    hunter: bool = Field(None, alias="hunter")
    quake: bool = Field(None, alias="quake")
    ip_input: str = Field(None, alias="ip_input")
    port_scanning: bool = Field(None, alias="port_scanning")
    default_ports_input: str = Field(None, alias="default_ports_input")
    custom_ports_input: str = Field(None, alias="custom_ports_input")
    service_identification: bool = Field(None, alias="service_identification")
    fingerprint_identification: bool = Field(None, alias="fingerprint_identification")
    weak_password_detection: bool = Field(None, alias="weak_password_detection")
    poc_scanning: bool = Field(None, alias="poc_scanning")

# 设置请求接收字段
class TaskSchemaIn(ModelSchema):
    class Config:
        model = Task
        model_fields = ['task_name', 'project_uuid', 'task_desc', 'task_type', 'task_status', 'full_company_name_input', 'root_domain_input', 'ip_input', 'domain_brute_force', 'historical_domain_query', 'port_scanning', 'framework_identification', 'fingerprint_identification', 'fofa', 'hunter', 'quake', 'ip_input', 'port_scanning', 'default_ports_input', 'custom_ports_input', 'service_identification', 'fingerprint_identification', 'weak_password_detection', 'poc_scanning']


# 设置响应字段
class TaskSchemaOut(ModelSchema):
    class Config:
        model = Task
        model_fields = "__all__"

# 创建Task
@router.post("/", response=TaskSchemaOut)
def create_demo(request, data: TaskSchemaIn):
    project = Project.objects.get(uuid=data.project_uuid)
    data.project_uuid = project
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

