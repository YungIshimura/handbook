# Generated by Django 3.2.10 on 2023-03-06 11:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo_handbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branches',
            name='postcode',
            field=models.PositiveBigIntegerField(validators=[django.core.validators.MaxValueValidator(999999)], verbose_name='Почтовый индекс'),
        ),
        migrations.AlterField(
            model_name='company',
            name='inn',
            field=models.PositiveBigIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)], verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='company',
            name='ogrn',
            field=models.PositiveBigIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999999)], verbose_name='ОГРН/ОГРНИП'),
        ),
    ]
