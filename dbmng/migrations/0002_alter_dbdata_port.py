# Generated by Django 3.2.14 on 2022-08-31 13:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmng', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbdata',
            name='PORT',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(65535)], verbose_name='连接端口'),
        ),
    ]