# Generated by Django 4.0.5 on 2022-07-26 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0015_remove_counterparty_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='counterparty',
            name='type',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
