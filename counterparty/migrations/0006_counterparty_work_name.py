# Generated by Django 4.0.5 on 2022-08-19 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counterparty', '0005_delete_counterpartyto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='counterparty',
            name='work_name',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]
