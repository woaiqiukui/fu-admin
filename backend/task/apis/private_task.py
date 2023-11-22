from typing import List
import uuid
from django.http import JsonResponse
from ninja import Router, ModelSchema, Query, Field
from ninja.pagination import paginate
from project.models import Project
from ..tasks import portScan
from utils.yunying_crud import create, delete, update, retrieve, ImportSchema, export_data, import_data
from utils.fu_ninja import YunYingFilters, MyPagination
from ..models import Port, Task

router = Router()

@router.post("/{task_uuid}")
def getTaskResult(request, task_uuid: uuid.UUID):
    try:
        # 获取项目名称
        project = Task.objects.get(uuid=task_uuid).project_uuid
        project_name = project.project_name
        # 获取该项目的所有任务名称及 task_uuid
        task_list_name_and_uuid = Task.objects.filter(project_uuid=project.uuid).values('task_name', 'uuid')

        # 获取 task_uuid 下 task 所有信息
        task_result = Task.objects.filter(uuid=task_uuid).values()

        # 获取该任务下所有端口信息
        port_result = Port.objects.filter(task_uuid_id=task_uuid).values()

        
        # 构建返回的 JSON 字典
        result_data = {
            'project_name': project_name,
            'task_list_name_and_uuid': list(task_list_name_and_uuid),
            'task_result': list(task_result),
            'port_result': list(port_result),
        }

        # print(result_data)
        # 返回 JSON 响应
        return result_data

    except (Task.DoesNotExist, Project.DoesNotExist) as e:
        # 处理对象不存在的情况
        return JsonResponse({'error': str(e)}, status=404)
