# Generated by Django 4.0.5 on 2022-07-28 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0020_alter_counterpartyto_options_remove_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='business_trip',
            field=models.BooleanField(default=False),
        ),
    ]
