# Generated by Django 4.0.5 on 2022-07-04 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_alter_worktask_options_alter_worktask_date_work_task_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worktask',
            name='date_work_task',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='worktask',
            name='time_work_task',
            field=models.TimeField(),
        ),
    ]
