from django.db import models


# Таблица задач
class Task(models.Model):
    date_task = models.DateField()
    time_task = models.TimeField()
    text_task = models.TextField()
    object_task = models.CharField(max_length=500, default="Офис Эртел")
    address_obj_task = models.CharField(max_length=500, default="")
    author_task = models.CharField(max_length=120)
    employee_task = models.CharField(max_length=120)
    urgency_task = models.CharField(max_length=150, default="")
    line_task = models.DateField(max_length=150)
    status_task = models.CharField(max_length=150, default="Отдано в разработку")
    business_trip = models.CharField(max_length=150, default="Не командировка")
    type_task = models.CharField(max_length=150, default="Офис")
    note_task = models.CharField(max_length=250, default="")
    datetime_note_task = models.DateTimeField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"id:{self.id} date: {self.date_task} time: {self.time_task} text: {self.text_task}"

    class Meta:
        verbose_name = "задачу"
        verbose_name_plural = 'задачи'


class TypeWork(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "тип работы"
        verbose_name_plural = "тип работ"


class BestEmployee(models.Model):
    date_be = models.DateField(blank=True, null=True)
    employee_be = models.CharField(max_length=120)
    time_do_object = models.CharField(max_length=200, default="00:00:00")
    time_on_object = models.CharField(max_length=200, default="00:00:00")
