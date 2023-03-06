from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator


class User(AbstractUser):
    bank_account = models.PositiveIntegerField( # TODO валидатор для расчётного счёта 
        'Расчётный счёт',
        validators=[MaxValueValidator(99999999999999999999)]
    )
    bik = models.PositiveIntegerField( # TODO валидатор для БИК
        'БИК',
        validators=[MaxValueValidator(999999999)]
    )
    bank_name = models.CharField(
        'Название банка',
        max_length=30
    )
