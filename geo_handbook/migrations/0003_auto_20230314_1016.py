# Generated by Django 3.2.10 on 2023-03-14 07:16

import django.contrib.postgres.fields
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('geo_handbook', '0002_auto_20230314_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='email',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254, verbose_name='Электронная почта'), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='employee',
            name='phonenumber',
            field=django.contrib.postgres.fields.ArrayField(base_field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона'), blank=True, null=True, size=None),
        ),
    ]
