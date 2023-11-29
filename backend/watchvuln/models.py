# watchvuln/models.py

from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _

class WebhookEvent(models.Model):
    # 字段定义
    key = models.CharField(_('Key'), max_length=255, blank=True, null=True)
    title = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    severity = models.CharField(_('Severity'), max_length=20, blank=True, null=True)
    cve = models.CharField(_('CVE'), max_length=30, blank=True, null=True)
    disclosure = models.DateField(_('Disclosure Date'), blank=True, null=True)
    solutions = models.TextField(_('Solutions'), blank=True, null=True)
    references = models.JSONField(_('References'), blank=True, null=True)
    tags = models.JSONField(_('Tags'), blank=True, null=True)
    github_search = models.CharField(_('GitHub Search'), max_length=255, blank=True, null=True)
    from_source = models.CharField(_('From Source'), max_length=255, blank=True, null=True, db_column='from')
    pushed = models.DateTimeField(_('Pushed'), blank=True, null=True)
    create_time = models.DateTimeField(_('Create Time'), default=timezone.now)
    update_time = models.DateTimeField(_('Update Time'), default=timezone.now)

    # 添加其他字段根据需要

    def __str__(self):
        return f'{self.event_type} - {self.create_time}'

    class Meta:
        db_table = 'vuln_informations'
        verbose_name = _('Webhook Event')
        verbose_name_plural = _('Webhook Events')
