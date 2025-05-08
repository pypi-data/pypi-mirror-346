from django.db import models
from django.conf import settings


class UserActivity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    request_data = models.JSONField(null=True, blank=True)
    response_status = models.IntegerField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    operation_type = models.CharField(
        max_length=10,
        choices=[
            ('CREATE', 'Create'),
            ('READ', 'Read'),
            ('UPDATE', 'Update'),
            ('DELETE', 'Delete'),
        ],
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.user.username if self.user else 'Anonymous'
        return f"{user_str} - {self.method} {self.path} ({self.timestamp})"
