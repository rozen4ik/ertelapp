# Generated by Django 4.0.5 on 2022-07-26 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0016_counterparty_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='address_task',
            field=models.CharField(default='Офис Эртел', max_length=500),
        ),
    ]
