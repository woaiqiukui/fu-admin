from django.db import models
from project.models import Project
from utils.models import yunyingModel, resultModel

class Task(yunyingModel):
    task_name = models.CharField(null=False, max_length=64, verbose_name="任务名称")
    project_uuid = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目ID")
    task_desc = models.CharField(max_length=128, verbose_name="任务描述")
    task_type = models.CharField(max_length=128, verbose_name="任务类型")
    task_status = models.CharField(max_length=128, verbose_name="任务状态")

    # 公网资产监控
    public_full_company_name_input = models.CharField(default="", max_length=128, verbose_name="公司全称")
    public_root_domain_input = models.CharField(default="", max_length=128, verbose_name="根域名")
    public_ip_input = models.CharField(default="", max_length=128, verbose_name="IP地址")
    public_domain_brute_force = models.BooleanField(default=False, verbose_name="域名暴力破解")
    public_historical_domain_query = models.BooleanField(default=False, verbose_name="历史域名查询")
    public_port_scanning = models.BooleanField(default=False, verbose_name="端口扫描")
    public_fingerprint_identification = models.BooleanField(default=False, verbose_name="指纹识别")
    public_fofa = models.BooleanField(default=False, verbose_name="fofa")
    public_hunter = models.BooleanField(default=False, verbose_name="hunter")
    public_quake = models.BooleanField(default=False, verbose_name="quake")

    # 内网资产扫描
    private_ip_input = models.CharField(default="", max_length=128, verbose_name="IP地址")
    private_port_scanning = models.CharField(default="", max_length=128, verbose_name="端口扫描类型")
    private_default_ports_input = models.CharField(default="", max_length=128, verbose_name="默认端口列表")
    private_custom_ports_input = models.CharField(default="", max_length=128, verbose_name="自定义端口列表")
    private_fingerprint_identification = models.BooleanField(default=False, verbose_name="指纹识别")
    private_weak_password_detection = models.BooleanField(default=False, verbose_name="弱口令探测")
    private_poc_scanning = models.BooleanField(default=False, verbose_name="POC扫描")

    class Meta:
        db_table = "task_task"
        verbose_name = "任务信息"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class Port(resultModel):
    task_uuid = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="任务UUID")
    ip = models.CharField(max_length=128, verbose_name="IP地址")
    port = models.CharField(max_length=128, verbose_name="端口")
    tag = models.CharField(max_length=128, verbose_name="标签")

    class Meta:
        db_table = "task_port"
        verbose_name = "端口信息"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

