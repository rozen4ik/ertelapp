# Generated by Django 4.0.5 on 2022-10-19 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0017_typework'),
    ]

    operations = [
        migrations.CreateModel(
            name='BestEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_be', models.DateField()),
                ('employee_be', models.CharField(max_length=120)),
                ('time_do_object', models.CharField(max_length=200)),
                ('time_on_object', models.CharField(max_length=200)),
            ],
        ),
    ]
