from django.db import models
from project.models import Project
from utils.models import yunyingModel

class Task(yunyingModel):
    task_name = models.CharField(null=False, max_length=64, verbose_name="任务名称")
    project_uuid = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目ID")
    task_desc = models.CharField(max_length=128, verbose_name="任务描述")
    task_type = models.CharField(max_length=128, verbose_name="任务类型")
    task_status = models.CharField(max_length=128, verbose_name="任务状态")

    # 公网资产监控
    full_company_name_input = models.CharField(default="", max_length=128, verbose_name="公司全称")
    root_domain_input = models.CharField(default="", max_length=128, verbose_name="根域名")
    ip_input = models.CharField(default="", max_length=128, verbose_name="IP地址")
    domain_brute_force = models.BooleanField(default=False, verbose_name="域名暴力破解")
    historical_domain_query = models.BooleanField(default=False, verbose_name="历史域名查询")
    framework_identification = models.BooleanField(default=False, verbose_name="框架识别")
    fingerprint_identification = models.BooleanField(default=False, verbose_name="指纹识别")
    fofa = models.BooleanField(default=False, verbose_name="fofa")
    hunter = models.BooleanField(default=False, verbose_name="hunter")
    quake = models.BooleanField(default=False, verbose_name="quake")

    # 内网资产扫描
    ip_input = models.CharField(default="", max_length=128, verbose_name="IP地址")
    port_scanning = models.CharField(default="", max_length=128, verbose_name="端口扫描类型")
    default_ports_input = models.CharField(default="", max_length=128, verbose_name="默认端口列表")
    custom_ports_input = models.CharField(default="", max_length=128, verbose_name="自定义端口列表")
    service_identification = models.BooleanField(default=False, verbose_name="服务识别")
    fingerprint_identification = models.BooleanField(default=False, verbose_name="指纹识别")
    weak_password_detection = models.BooleanField(default=False, verbose_name="弱口令探测")
    poc_scanning = models.BooleanField(default=False, verbose_name="POC扫描")

    class Meta:
        db_table = "task_task"
        verbose_name = "任务信息"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)