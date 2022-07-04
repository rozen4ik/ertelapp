# Generated by Django 4.0.5 on 2022-07-04 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_profile_chat_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
        migrations.CreateModel(
            name='WorkTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_work_task', models.DateField()),
                ('time_work_task', models.TimeField()),
                ('employee_work_task', models.CharField(max_length=120)),
                ('address_work_task', models.CharField(max_length=500)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task')),
            ],
            options={
                'verbose_name': 'Учёт рабочего времени',
                'verbose_name_plural': 'Учёт рабочики времени',
            },
        ),
    ]