from django.db import models
from task.models import Task


class WorkTask(models.Model):
    date_work_task = models.DateField()
    time_work_task = models.TimeField()
    employee_work_task = models.CharField(max_length=120)
    address_work_task = models.CharField(max_length=500)
    status_work_task = models.CharField(max_length=120)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Исполнитель: {self.employee_work_task} Место нахождение: {self.task}"

    class Meta:
        verbose_name = "учёт рабочего времени"
        verbose_name_plural = "учёт рабочего времени"
