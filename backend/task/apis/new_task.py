from typing import List
import uuid
from ninja import Router, ModelSchema, Query, Field
from ninja.pagination import paginate
from project.models import Project
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

    public_full_company_name_input: str = Field(None, alias="public_full_company_name_input")
    public_root_domain_input: str = Field(None, alias="public_root_domain_input")
    public_ip_input: str = Field(None, alias="public_ip_input")
    public_domain_brute_force: bool = Field(None, alias="public_domain_brute_force")
    public_historical_domain_query: bool = Field(None, alias="public_historical_domain_query")
    public_port_scanning: bool = Field(None, alias="public_port_scanning")
    public_fingerprint_identification: bool = Field(None, alias="public_fingerprint_identification")
    public_fofa: bool = Field(None, alias="public_fofa")
    public_hunter: bool = Field(None, alias="public_hunter")
    public_quake: bool = Field(None, alias="public_quake")
    
    private_ip_input: str = Field(None, alias="private_ip_input")
    private_port_scanning: bool = Field(None, alias="private_port_scanning")
    private_default_ports_input: str = Field(None, alias="private_default_ports_input")
    private_custom_ports_input: str = Field(None, alias="private_custom_ports_input")
    private_fingerprint_identification: bool = Field(None, alias="private_fingerprint_identification")
    private_weak_password_detection: bool = Field(None, alias="private_weak_password_detection")
    private_poc_scanning: bool = Field(None, alias="private_poc_scanning")

# 设置请求接收字段
class TaskSchemaIn(ModelSchema):
    class Config:
        model = Task
        model_fields = ['task_name', 
                        'project_uuid', 
                        'task_desc', 
                        'task_type', 
                        'task_status', 

                        'public_full_company_name_input', 
                        'public_root_domain_input', 
                        'public_ip_input', 
                        'public_domain_brute_force', 
                        'public_historical_domain_query', 
                        'public_port_scanning', 
                        'public_fingerprint_identification', 
                        'public_fofa', 
                        'public_hunter', 
                        'public_quake', 

                        'private_ip_input', 
                        'private_port_scanning', 
                        'private_default_ports_input', 
                        'private_custom_ports_input', 
                        'private_fingerprint_identification', 
                        'private_weak_password_detection', 
                        'private_poc_scanning']


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
    # 判断任务类型并分发异步任务
    # if task.task_type == '1':
    #     public_task.delay(str(task.uuid))
    # elif task.task_type == '2':
    #     if (task.private_port_scanning == 'custom'):
    #         portScan.delay(task.private_ip_input, task.private_custom_ports_input, task.uuid)
    #     else:
    #         portScan.delay(task.private_ip_input, task.private_default_ports_input, task.uuid)
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

# 获取Task Detail
@router.get("/{task_uuid}", response=TaskSchemaOut)
def get_demo_detail(request, task_uuid: uuid.UUID):
    return retrieve(request, Task, task_uuid)
