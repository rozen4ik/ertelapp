# Generated by Django 4.0.5 on 2022-08-04 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_work_task', models.DateField()),
                ('time_work_task', models.TimeField()),
                ('employee_work_task', models.CharField(max_length=120)),
                ('address_work_task', models.CharField(max_length=500)),
                ('status_work_task', models.CharField(max_length=120)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task')),
            ],
            options={
                'verbose_name': 'учёт рабочего времени',
                'verbose_name_plural': 'учёт рабочего времени',
            },
        ),
    ]
