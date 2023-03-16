# Generated by Django 3.2.10 on 2023-03-16 05:51

import django.contrib.postgres.fields
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('geo_handbook', '0003_auto_20230314_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='contact_email',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254, verbose_name='Электронная почта(пользователь)'), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='company',
            name='contact_phone',
            field=django.contrib.postgres.fields.ArrayField(base_field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона(пользователь)'), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='company',
            name='contact_url',
            field=models.URLField(blank=True, max_length=128, null=True, verbose_name='Сайт компании(пользователь)'),
        ),
    ]