# Generated by Django 4.0.5 on 2022-07-26 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0013_alter_task_status_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counterparty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('type', models.CharField(max_length=150)),
                ('contract', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Контрагент',
                'verbose_name_plural': 'Контрагенты',
            },
        ),
    ]
