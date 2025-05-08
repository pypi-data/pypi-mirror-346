from django.apps import AppConfig


class IntegrationLoggerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integration_logger'
    verbose_name = 'User Activity Logger'
