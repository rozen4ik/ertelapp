from django.db import models


# Таблица задач
class Task(models.Model):
    date_task = models.DateField()
    time_task = models.TimeField()
    text_task = models.TextField()
    address_task = models.CharField(max_length=500, default="Офис Эртел")
    author_task = models.CharField(max_length=120)
    employee_task = models.CharField(max_length=120)
    line_task = models.DateField(max_length=150)
    status_task = models.CharField(max_length=150, default="Отдано в разработку")
    business_trip = models.CharField(max_length=150, default="Не командировка")
    type_task = models.CharField(max_length=150, default="Офис")

    def __str__(self):
        return f"{self.text_task}"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = 'Задачи'
