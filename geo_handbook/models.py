from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class TypeWork(models.Model):
    type = models.CharField(
        'Тип работы',
        max_length=50
    )

    def __str__(self):
        return f'{self.type}'

    class Meta:
        verbose_name = 'Тип работы'
        verbose_name_plural = 'Типы работ'


class CompanyAddress(models.Model):
    city = models.CharField(
        'Город нахождения компании',
        max_length=50
    )
    postcode = models.PositiveIntegerField(
        'Почтовый индес',
        validators=[MaxValueValidator(999999)]
    )
    region = models.CharField(
        'Субъект РФ',
        max_length=120,
        blank=True,
        null=True
    )
    district = models.CharField(
        'Район города',
        max_length=100,
        blank=True,
        null=True
    )
    street = models.CharField(
        'Улица',
        max_length=150,
    )
    house_number = models.PositiveIntegerField(
        'Номер дома'
    )
    is_legal = models.BooleanField(
        'Юридический адрес компании',
        default=False
    )

    def __str__(self):
        return self.city


class SRO(models.Model):
    full_name = models.CharField(
        'Название СРО',
        max_length=500
    )

    short_name = models.CharField(
        'Название СРО сокращенное',
        max_length=100,
        null=True,
        blank=True
    )

    number = models.CharField(
        'Номер СРО',
        max_length=18,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.short_name} {self.number}'

    class Meta:
        verbose_name = 'Саморегулируемая организация'
        verbose_name_plural = 'Саморегулируемые организации'


class Company(models.Model):
    short_name = models.CharField(
        'Короткое название компании',
        max_length=100
    )
    full_name = models.CharField(
        'Полное название компании',
        max_length=250
    )
    firm_name = models.CharField(
        'Фирменное наименование',
        max_length=250,
        blank=True,
        null=True
    )
    address = models.ForeignKey(
        CompanyAddress,
        related_name='companys',
        on_delete=models.CASCADE,
        verbose_name='Место',
        blank=True,
        null=True
    )
    rating = models.PositiveIntegerField(
        'Рейтинг компании',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    inn = models.PositiveBigIntegerField(  # TODO написать валидатор для ИНН компании
        'ИНН',
        validators=[MaxValueValidator(999999999999)]
    )
    ogrn = models.PositiveBigIntegerField(  # TODO написать валидатор для ОГРН компании
        'ОГРН/ОГРНИП',
        validators=[MaxValueValidator(999999999999999)]
    )
    sro = models.ForeignKey(
        SRO,
        related_name='companys',
        on_delete=models.PROTECT,
        verbose_name='СРО'
    )
    sro_date = models.DateField(
        'Дата приёма в члены СРО',
        blank=True,
        null=True
    )
    sro_number = models.CharField(
        'Номер решения о приёме в члены СРО',
        max_length=25,
        blank=True,
        null=True
    )
    license = models.BooleanField(
        'Наличие лицензии',
        default=True
    )
    license_date = models.DateField(
        'Дата прикращения членства',
        blank=True,
        null=True
    )
    phonenumber = PhoneNumberField(
        verbose_name='Номер телефона',
        db_index=True,
        blank=True,
        null=True
    )
    email = models.EmailField(
        'Электронная почта'
    )
    url = models.URLField(
        'Сайт компании',
        max_length=128,
    )

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Branches(models.Model):
    address = models.ForeignKey(
        CompanyAddress,
        on_delete=models.CASCADE,
        related_name='branches',
        verbose_name='Aдресс',
        blank=True,
        null=True
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='branches',
        verbose_name='Компания'
    )

    def __str__(self):
        return f'Филиал компании - {self.company} {self.address}'

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


class CompanySpecialization(models.Model):
    type_work = models.ForeignKey(
        TypeWork,
        related_name='work_types',
        on_delete=models.PROTECT,
        verbose_name='Тип работ'
    )
    company = models.ForeignKey(
        Company,
        related_name='specializations',
        on_delete=models.CASCADE,
        verbose_name='Компания'
    )

    def __str__(self):
        return f'{self.type_work} - {self.company}'

    class Meta:
        verbose_name = 'Специализация компании'
        verbose_name_plural = 'Специализации компаний'


class Director(models.Model):
    name = models.CharField(
        'Имя руководителя',
        max_length=20
    )
    surname = models.CharField(
        'Фамилия руководителя',
        max_length=50
    )
    father_name = models.CharField(
        'Отчество руководителя',
        max_length=30
    )
    position = models.CharField(
        'Должность руководителя',
        max_length=50
    )
    company = models.ForeignKey(
        Company,
        related_name='director',
        on_delete=models.CASCADE,
        verbose_name='Компания',
        blank=True,
        null=True
    )
    branches = models.ForeignKey(
        Branches,
        related_name='director',
        on_delete=models.CASCADE,
        verbose_name='Филиал',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name} {self.surname} {self.father_name} - {self.company}'

    class Meta:
        verbose_name = 'Директор'
        verbose_name_plural = 'Директора'


class Employee(models.Model):
    name = models.CharField(
        'Имя сотрудника',
        max_length=20
    )
    surname = models.CharField(
        'Фамилия сотрудника',
        max_length=50
    )
    father_name = models.CharField(
        'Отчество сотрудника',
        max_length=30
    )
    position = models.CharField(
        'Должность сотрудника',
        max_length=50
    )
    company = models.ForeignKey(
        Company,
        related_name='employee',
        on_delete=models.CASCADE,
        verbose_name='Компания',
        blank=True,
        null=True
    )
    branches = models.ForeignKey(
        Branches,
        related_name='employee',
        on_delete=models.CASCADE,
        verbose_name='Филиал',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Сотрудник {self.name} {self.surname} {self.father_name}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудник'
