from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
from smart_selects.db_fields import ChainedForeignKey


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


class Region(models.Model):
    name = models.CharField(
        'Название региона',
        max_length=180
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class Area(models.Model):
    name = models.CharField(
        'Название района',
        max_length=200
    )
    region = models.ForeignKey(
        Region,
        related_name='areas',
        on_delete=models.CASCADE,
        verbose_name='Регион',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class City(models.Model):
    name = models.CharField(
        'Название города',
        max_length=100
    )
    area = models.ForeignKey(
        Area,
        related_name='citys',
        on_delete=models.CASCADE,
        verbose_name='Район',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class CompanyAddress(models.Model):
    city = models.ForeignKey(
        City,
        related_name='companys',
        on_delete=models.CASCADE,
        verbose_name='Город нахождения компании',
        max_length=50
    )
    region = models.ForeignKey(
        Region,
        related_name='companys',
        on_delete=models.CASCADE,
        max_length=120,
        blank=True,
        null=True
    )
    postcode = models.PositiveIntegerField(
        'Почтовый индекс',
        validators=[MaxValueValidator(999999)]
    )
    district = models.CharField(
        'Район города',
        max_length=100,
    )
    street = models.CharField(
        'Улица',
        max_length=150,
    )
    house_number = models.PositiveIntegerField(
        'Номер дома'
    )

    def __str__(self):
        return f'{self.city} {self.region} - {self.postcode}'

    class Meta:
        verbose_name = 'Адрес компании'
        verbose_name_plural = 'Адреса компаний'


class SRO(models.Model):
    full_name = models.CharField(
        'Название СРО полное',
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
    legal_address = models.ForeignKey(
        CompanyAddress,
        related_name='companys',
        on_delete=models.CASCADE,
        verbose_name='Юридический адрес',
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
        verbose_name='СРО',
        blank=True,
        null=True
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
    phonenumber = ArrayField(PhoneNumberField(
        verbose_name='Номер телефона',
        db_index=True,
    ),
        blank=True,
        null=True)
    email = ArrayField(models.EmailField(
        'Электронная почта'
    ),
        blank=True,
        null=True)
    url = ArrayField(models.URLField(
        'Сайт компании',
        max_length=128,
    ),
        blank=True,
        null=True)
    contact_phone = ArrayField(PhoneNumberField(
        verbose_name='Номер телефона(пользователь)',
    ),
        blank=True,
        null=True)
    contact_email = ArrayField(models.EmailField(
        'Электронная почта(пользователь)'
    ),
        blank=True,
        null=True)
    contact_url = models.URLField(
        'Сайт компании(пользователь)',
        max_length=128,
        blank=True,
        null=True)

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class License(models.Model):
    name = models.CharField(
        'Название лицензии',
        max_length=250
    )
    license_date = models.DateField(
        'Срок действия лицензии'
    )
    license_area = models.CharField(
        'Область применения лицензии',
        max_length=250
    )
    license_organization = models.CharField(
        'Организация выдавшая лицензию',
        max_length=250
    )
    company = models.ForeignKey(
        Company,
        related_name='licenses',
        on_delete=models.PROTECT,
        verbose_name='Компания',
    )


class Branches(models.Model):
    address = models.ForeignKey(
        CompanyAddress,
        on_delete=models.CASCADE,
        related_name='branches',
        verbose_name='Aдресс',
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='branches',
        verbose_name='Компания'
    )

    def __str__(self):
        return f'Филиал компании - {self.company}'

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
    phonenumber = ArrayField(PhoneNumberField(
        'Номер телефона',
    ),
        blank=True,
        null=True)
    email = ArrayField(models.EmailField(
        'Электронная почта'
    ),
        blank=True,
        null=True)
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


class Order(models.Model):
    STATUS = (
        ('processed', 'Обработанная'),
        ('not processed', 'Не обработанная')
    )
    name = models.CharField(
        'Имя заказчика',
        max_length=100,
        blank=True
    )
    surname = models.CharField(
        'Фамилия заказчика',
        max_length=250,
        blank=True
    )
    father_name = models.CharField(
        'Отчество заказчика',
        max_length=250,
        blank=True
    )
    phone_number = PhoneNumberField(
        blank=True
    )
    email = models.EmailField(
        "Электронная почта заказчика",
        max_length=254,
        blank=True
    )
    cadastral_number = models.CharField(
        'Кадастровый номер',
        max_length=50,
    )
    region = models.ForeignKey(
        Region,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='Регион'
    )
    area = ChainedForeignKey(
        Area,
        blank=True,
        null=True,
        chained_field='region',
        chained_model_field='region',
        show_all=False,
        auto_choose=True,
        sort=True
    )
    city = ChainedForeignKey(
        City,
        chained_field='area',
        chained_model_field='area',
        show_all=False,
        auto_choose=True,
        sort=True
    )
    street = models.CharField(
        'Улица',
        max_length=250,
    )
    house_number = models.PositiveIntegerField(
        'Номер дома',
        validators=[MinValueValidator(0)]
    )
    building = models.PositiveBigIntegerField(
        'Строение/Корпус',
        validators=[MinValueValidator(0)]
    )
    square = models.PositiveIntegerField(
        'Площадь участка',
        validators=[MinValueValidator(0)]
    )
    length = models.PositiveIntegerField(
        'Длина',
        validators=[MinValueValidator(0)]
    )
    heigth = models.PositiveIntegerField(
        'Высота',
        validators=[MinValueValidator(0)]
    )
    width = models.PositiveIntegerField(
        'Ширина',
        validators=[MinValueValidator(0)]
    )
    type_work = models.ForeignKey(
        TypeWork,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='Тип работы',
        blank=True,
        null=True
    )
    title = models.TextField(
        'Навзание объекта'
    )
    status = models.CharField(
        'Статус заказа',
        max_length=100,
        choices=STATUS,
        blank=True,
        default='not processed'
    )


class OrderFiles(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Заказы'
    )
    file = models.FileField(
        'Файл'
    )


class WorkRegion(models.Model):
    title = models.CharField(
        'название субъекта',
        max_length=50
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Регион работ'
        verbose_name_plural = 'Регионы работ'


class CompanyWorkRegion(models.Model):
    working_zone = models.ForeignKey(
        WorkRegion,
        related_name='company_work_regions',
        on_delete=models.PROTECT,
        verbose_name='Регион выполняемых работ'
    )
    company = models.ForeignKey(
        Company,
        related_name='work_regions_companies',
        on_delete=models.CASCADE,
        verbose_name='Компания'
    )

    def __str__(self):
        return f'{self.working_zone} - {self.company}'

    class Meta:
        verbose_name = 'Регион работ компаний'
        verbose_name_plural = 'Регионы работ компаний'
