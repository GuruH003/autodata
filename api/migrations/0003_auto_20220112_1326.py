# Generated by Django 3.0.7 on 2022-01-12 13:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220112_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='modules',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), blank=True, default=list, null=True, size=None),
        ),
    ]