# Generated by Django 4.0.5 on 2022-07-28 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0019_countrpartywarrantyobligations_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='counterpartyto',
            options={'verbose_name': 'Контрагент: техническое обслуживание', 'verbose_name_plural': 'Контрагенты: техническое обслуживание'},
        ),
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
    ]
