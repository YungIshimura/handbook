from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_cadastral_number(value):
    validate_number_status=re.fullmatch(r'[0-9]{2}:[0-9]{2}:[0-9]{7}:[0-9]{3}', value)
    if not validate_number_status or len(validate_number_status)!=17:
        raise ValidationError(
            _('%(value)s - неверный номер. Убедитесь в правильности написани'),
            params={'value': value},
        )