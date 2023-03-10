# Generated by Django 3.2.10 on 2023-03-14 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo_handbook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sro',
            name='number',
            field=models.CharField(blank=True, max_length=18, null=True, verbose_name='Номер СРО'),
        ),
        migrations.AddField(
            model_name='sro',
            name='short_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Название СРО сокращенное'),
        ),
        migrations.AlterField(
            model_name='license',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='licenses', to='geo_handbook.company', verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='sro',
            name='full_name',
            field=models.CharField(max_length=500, verbose_name='Название СРО полное'),
        ),
    ]
