# Generated by Django 4.0.5 on 2022-08-10 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('counterparty', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='counterpartyto',
            options={'verbose_name': 'техническое обслуживание', 'verbose_name_plural': 'техническое обслуживание'},
        ),
        migrations.AlterModelOptions(
            name='counterpartywarrantyobligations',
            options={'verbose_name': 'гарантийные обязательства', 'verbose_name_plural': 'гарантийные обязательства'},
        ),
    ]