from django.apps import AppConfig


class WorkTaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'work_task'
    verbose_name = "контроль выполнения работ"
    verbose_name_plural = "контроль выполнения работ"
