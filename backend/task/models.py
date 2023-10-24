from django.db import models
from project.models import Project
from utils.models import CoreModel

class Task(models.Model):
    task_name = models.CharField(null=False, max_length=64, verbose_name="任务名称")
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目ID")
    task_desc = models.CharField(max_length=128, verbose_name="任务描述")
    task_type = models.CharField(max_length=128, verbose_name="任务类型")
    task_status = models.CharField(max_length=128, verbose_name="任务状态")

