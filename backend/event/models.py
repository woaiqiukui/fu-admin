from django.db import models
from django.utils.translation import gettext_lazy as _

class SecurityIntelligence(models.Model):
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)  # Added url field

    # 添加其他字段根据需要

    class Meta:
        db_table = 'security_intelligence'
        verbose_name = _('Security Intelligence Event')
        verbose_name_plural = _('Security Intelligence Events')
