# Generated by Django 4.0.5 on 2022-07-05 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_rename_position_id_profile_position_dep_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='position_dep_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='task.position'),
        ),
    ]
