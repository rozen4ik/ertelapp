# Generated by Django 4.0.5 on 2022-08-05 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_alter_task_datetime_note_task_alter_task_note_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='datetime_note_task',
            field=models.DateField(blank=True, max_length=150),
        ),
    ]
