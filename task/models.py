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

    class Meta:
        verbose_name = 'Задачу'
        verbose_name_plural = 'Задачи'


# Таблица профиля связа с таблицей User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=150)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()