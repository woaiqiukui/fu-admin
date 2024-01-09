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
    address = models.CharField(max_length=128, verbose_name="IP地址")
    port = models.CharField(max_length=128, verbose_name="端口")
    protocol = models.CharField(max_length=128, verbose_name="协议", default="Unknown")
    state = models.CharField(max_length=128, verbose_name="状态", default="Unknown")
    service = models.CharField(max_length=128, verbose_name="服务", default="Unknown")
    product = models.CharField(max_length=128, verbose_name="产品", default="Unknown")
    version = models.CharField(max_length=128, verbose_name="版本", default="Unknown")

    class Meta:
        db_table = "task_port"
        verbose_name = "端口信息"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Url(resultModel):
    task_uuid = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="任务UUID")
    port = models.CharField(max_length=128, verbose_name="端口")
    url = models.CharField(max_length=128, verbose_name="URL")
    title = models.CharField(max_length=128, verbose_name="标题", default="Unknown")
    scheme = models.CharField(max_length=128, verbose_name="协议", default="Unknown")
    webserver = models.CharField(max_length=128, verbose_name="Web服务器", default="Unknown")
    content_type = models.CharField(max_length=128, verbose_name="内容类型", default="Unknown")
    method = models.CharField(max_length=128, verbose_name="请求方法", default="Unknown")
    host = models.CharField(max_length=128, verbose_name="主机", default="Unknown")
    path = models.CharField(max_length=128, verbose_name="路径", default="Unknown")
    time = models.CharField(max_length=128, verbose_name="响应时间", default="Unknown")
    status_code = models.CharField(max_length=128, verbose_name="状态码", default="Unknown")

    class Meta:
        db_table = "task_url"
        verbose_name = "URL信息"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class Finger(resultModel):
    task_uuid = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="任务UUID")
    url = models.CharField(max_length=128, verbose_name="URL")
    name = models.JSONField(verbose_name="名称", default=dict)
    priority = models.IntegerField(verbose_name="优先级", default=0)
    length = models.IntegerField(verbose_name="长度", default=0)
    title = models.CharField(max_length=128, verbose_name="标题", default="Unknown")
    status_code = models.IntegerField(verbose_name="状态码", default=0)
    is_web = models.BooleanField(verbose_name="是否为Web", default=False)

    class Meta:
        db_table = "task_finger"
        verbose_name = "指纹信息"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Nuclei(resultModel):
    task_uuid = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="任务UUID")
    template = models.CharField(max_length=128, verbose_name="模板")
    template_url = models.CharField(max_length=128, verbose_name="模板URL")
    template_id = models.CharField(max_length=128, verbose_name="模板ID")
    template_path = models.CharField(max_length=128, verbose_name="模板路径")
    template_encoded = models.TextField(verbose_name="模板编码")
    name = models.CharField(max_length=128, verbose_name="名称")
    author = models.CharField(max_length=128, verbose_name="作者", null=True)
    tags = models.CharField(max_length=128, verbose_name="标签", null=True)
    severity = models.CharField(max_length=128, verbose_name="严重程度")
    type = models.CharField(max_length=128, verbose_name="类型")
    host = models.CharField(max_length=128, verbose_name="主机")
    port = models.CharField(max_length=128, verbose_name="端口")
    scheme = models.CharField(max_length=128, verbose_name="协议")
    url = models.CharField(max_length=128, verbose_name="URL")
    matched_at = models.TextField(verbose_name="匹配特征")
    request = models.TextField(verbose_name="请求")
    response = models.TextField(verbose_name="响应")
    ip = models.CharField(max_length=128, verbose_name="IP")
    timestamp = models.CharField(max_length=128, verbose_name="时间戳")
    curl_command = models.TextField(verbose_name="CURL命令")
    matcher_status = models.BooleanField(verbose_name="匹配状态")

    class Meta:
        db_table = "task_poc_nuclei"
        verbose_name = "Nuclei扫描信息"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Xray(resultModel):
    task_uuid = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="任务UUID")
    create_time = models.BigIntegerField(verbose_name="创建时间")
    addr = models.CharField(max_length=256, verbose_name="地址")
    payload = models.CharField(max_length=256, verbose_name="负载")
    snapshot = models.JSONField(verbose_name="快照")
    extra = models.JSONField(verbose_name="额外信息")
    plugin = models.CharField(max_length=128, verbose_name="插件")
    url = models.CharField(max_length=256, verbose_name="目标URL")

    class Meta:
        db_table = "task_poc_xray"
        verbose_name = "Xray扫描信息"
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)


class Mail(resultModel):
    task_uuid = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="任务UUID")
    