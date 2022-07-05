from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Таблица задач
class Task(models.Model):
    date_task = models.DateField()
    time_task = models.TimeField()
    text_task = models.TextField()
    address_task = models.CharField(max_length=500)
    author_task = models.CharField(max_length=120)
    employee_task = models.CharField(max_length=120)
    line_task = models.CharField(max_length=150)
    status_task = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text_task}"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = 'Задачи'


# Таблица профиля связа с таблицей User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


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
        verbose_name = "Учёт рабочего времени"
        verbose_name_plural = "Учёт рабочего времени"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()