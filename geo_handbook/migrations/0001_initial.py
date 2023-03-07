# Generated by Django 3.2.10 on 2023-03-06 11:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postcode', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999999)], verbose_name='Почтовый индекс')),
                ('city', models.CharField(max_length=80, verbose_name='Город')),
                ('street', models.CharField(max_length=200, verbose_name='Улица')),
                ('house_number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Номер дома')),
            ],
            options={
                'verbose_name': 'Филиал',
                'verbose_name_plural': 'Филиалы',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=100, verbose_name='Короткое название компании')),
                ('full_name', models.CharField(max_length=250, verbose_name='Полное название компании')),
                ('firm_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Фирменное наименование')),
                ('city', models.CharField(max_length=30, verbose_name='Город')),
                ('area', models.CharField(max_length=80, verbose_name='Район')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Рейтинг компании')),
                ('inn', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)], verbose_name='ИНН')),
                ('ogrn', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999999)], verbose_name='ОГРН/ОГРНИП')),
                ('license', models.BooleanField(default=True, verbose_name='Наличие лицензии')),
                ('license_date', models.DateField(blank=True, null=True, verbose_name='Дата прикращения членства')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, db_index=True, max_length=128, null=True, region=None, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('url', models.URLField(max_length=128, verbose_name='Сайт компании')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.CreateModel(
            name='LegalAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postcode', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999999)], verbose_name='Почтовый индекс')),
                ('city', models.CharField(max_length=80, verbose_name='Город')),
                ('street', models.CharField(max_length=200, verbose_name='Улица')),
                ('house_number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Номер дома')),
            ],
            options={
                'verbose_name': 'Юр. адресс',
                'verbose_name_plural': 'Юр. адреса',
            },
        ),
        migrations.CreateModel(
            name='SRO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Название СРО')),
                ('date', models.DateField(verbose_name='Дата приёма в члены СРО')),
                ('number', models.CharField(max_length=25, verbose_name='Номер решения о приёме в члены СРО')),
            ],
            options={
                'verbose_name': 'Саморегулируемая организация',
                'verbose_name_plural': 'Саморегулируемые организации',
            },
        ),
        migrations.CreateModel(
            name='TypeWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50, verbose_name='Тип работы')),
            ],
            options={
                'verbose_name': 'Тип работы',
                'verbose_name_plural': 'Типы работ',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Имя сотрудника')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия сотрудника')),
                ('father_name', models.CharField(max_length=30, verbose_name='Отчество сотрудника')),
                ('position', models.CharField(max_length=50, verbose_name='Должность сотрудника')),
                ('branches', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='geo_handbook.branches', verbose_name='Филиал')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='geo_handbook.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудник',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Имя руководителя')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия руководителя')),
                ('father_name', models.CharField(max_length=30, verbose_name='Отчество руководителя')),
                ('position', models.CharField(max_length=50, verbose_name='Должность руководителя')),
                ('branches', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='director', to='geo_handbook.branches', verbose_name='Филиал')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='director', to='geo_handbook.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Директор',
                'verbose_name_plural': 'Директора',
            },
        ),
        migrations.CreateModel(
            name='CompanySpecialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialization', to='geo_handbook.company', verbose_name='Компания')),
                ('type_work', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company', to='geo_handbook.typework', verbose_name='Тип работ')),
            ],
            options={
                'verbose_name': 'Специализация компании',
                'verbose_name_plural': 'Специализации компаний',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='legal_address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='geo_handbook.legaladdress', verbose_name='Юридический адрес'),
        ),
        migrations.AddField(
            model_name='company',
            name='sro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='companys', to='geo_handbook.sro', verbose_name='СРО'),
        ),
        migrations.AddField(
            model_name='branches',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='geo_handbook.company', verbose_name='Компания'),
        ),
    ]