# Generated by Django 4.0.5 on 2022-08-05 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_alter_task_datetime_note_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='datetime_note_task',
        ),
    ]
