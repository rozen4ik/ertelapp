# Generated by Django 4.0.5 on 2022-10-20 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0018_bestemployee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bestemployee',
            name='time_do_object',
            field=models.CharField(default='00:00:00', max_length=200),
        ),
        migrations.AlterField(
            model_name='bestemployee',
            name='time_on_object',
            field=models.CharField(default='00:00:00', max_length=200),
        ),
    ]
