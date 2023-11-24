# watchvuln/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _

class WebhookEvent(models.Model):
    # 定义事件类型的选择项
    WATCHVULN_INITIAL = 'watchvuln-initial'
    WATCHVULN_TEXT = 'watchvuln-text'
    WATCHVULN_VULNINFO = 'watchvuln-vulninfo'

    EVENT_TYPE_CHOICES = [
        (WATCHVULN_INITIAL, _('WatchVuln Initialization')),
        (WATCHVULN_TEXT, _('WatchVuln Text')),
        (WATCHVULN_VULNINFO, _('WatchVuln Vulnerability Information')),
        # 如果有新的事件类型，可以在这里添加
    ]

    # 字段定义
    event_type = models.CharField(_('Event Type'), max_length=20, choices=EVENT_TYPE_CHOICES)
    unique_key = models.CharField(_('Unique Key'), max_length=255, blank=True, null=True)
    title = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    severity = models.CharField(_('Severity'), max_length=20, blank=True, null=True)
    cve = models.CharField(_('CVE'), max_length=30, blank=True, null=True)
    disclosure = models.DateField(_('Disclosure Date'), blank=True, null=True)
    solutions = models.TextField(_('Solutions'), blank=True, null=True)
    references = models.JSONField(_('References'), blank=True, null=True)
    tags = models.JSONField(_('Tags'), blank=True, null=True)
    from_source = models.CharField(_('From Source'), max_length=255, blank=True, null=True)
    reason = models.CharField(_('Reason'), max_length=255, blank=True, null=True)

    # 添加其他字段根据需要

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    def __str__(self):
        return f'{self.event_type} - {self.created_at}'

    class Meta:
        verbose_name = _('Webhook Event')
        verbose_name_plural = _('Webhook Events')
