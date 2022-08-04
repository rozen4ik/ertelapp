from django.db import models

from task.models import Task


class HistoryStatusTask(models.Model):
    datetime_history = models.DateTimeField()
    status_history = models.CharField(max_length=150)
    employee_history = models.CharField(max_length=150)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.datetime_history} {self.status_history} {self.employee_history} {self.task}"

    class Meta:
        verbose_name = "История изменения статуса задачи"
        verbose_name_plural = "История изменения статуса задач"


class HistoryNoteTask(models.Model):
    datetime_history = models.DateTimeField()
    note_history = models.CharField(max_length=150)
    employee_history = models.CharField(max_length=150)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.datetime_history} {self.note_history} {self.employee_history} {self.task}"

    class Meta:
        verbose_name = "История изменения примечания задачи"
        verbose_name_plural = "История изменения примечаний задач"
