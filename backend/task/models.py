from django.db import models
from utils.models import CoreModel

class Project(CoreModel):
    project_name = models.CharField(null=False, max_length=64, verbose_name="项目名称", help_text="项目名称")
    project_desc = models.CharField(max_length=128, verbose_name="项目描述", help_text="项目描述")
    project_status = models.BooleanField(verbose_name="项目状态", help_text="项目状态")

    class Meta:
        db_table = "task_project"
        verbose_name = "项目信息"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class PublicAsset(models.Model):
    asset_name = models.CharField(max_length=100, verbose_name="资产名称")
    root_domain_or_ip = models.TextField(verbose_name="根域名或IP列表")
    company_name = models.CharField(max_length=100, verbose_name="公司全称")
    additional_info = models.TextField(verbose_name="额外资产信息")
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目ID")

    class Meta:
        db_table = "public_assets"
        verbose_name = "公网资产信息"
        verbose_name_plural = verbose_name