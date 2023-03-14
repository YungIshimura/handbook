from django import forms
from geo_handbook.models import Company, Director, Employee, City, CompanyAddress
from django.core.exceptions import ValidationError


def validate_legal_address_postcode(value):
    if not value.isdigit() or len(value) != 6:
        raise ValidationError('Почтовый индекс должен содержать 6 цифр')


# форма редактирования данных о компании
class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


#     # Добавляем поля для редактирования связанных моделей
#     # legal_address_postcode = forms.CharField(
#     #     label='Почтовый индекс',
#     #     widget=forms.TextInput(attrs={'class': 'form-control'}),
#     #     validators=[validate_legal_address_postcode]
#     # )
#     # legal_address_city = forms.CharField(
#     #     label='Город',
#     #     widget=forms.TextInput(attrs={'class': 'form-control'})
#     # )
#     # legal_address_street = forms.CharField(
#     #     label='Улица',
#     #     widget=forms.TextInput(attrs={'class': 'form-control'})
#     # )
#     # legal_address_house_number = forms.CharField(
#     #     label='Номер дома',
#     #     widget=forms.TextInput(attrs={'class': 'form-control'})
#     # )
#     type_works = forms.ModelMultipleChoiceField(
#         label='Типы работ',
#         queryset=TypeWork.objects.all(),
#         widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'})
#     )

# class Meta:
#     model = Company
#     fields = ['type_works', 'short_name', 'inn', 'ogrn', 'legal_address', 'phonenumber', 'email', 'sro',
#               'sro_date', 'sro_number', 'license_date', 'url',
#               ]
#     widgets = {
#         'short_name': forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': 'ООО “Ромашка”'}),
#         'inn': forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': '525895655'}),
#         'ogrn': forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': '2624151254854561'}),
#         'legal_address': forms.HiddenInput(),
#         'phonenumber': forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': '+7 955 556 55 88'}),
#         'email': forms.EmailInput(
#             attrs={'class': 'form-control', 'placeholder': 'romashka@yandex.ru'}),
#         'sro': forms.Select(attrs={'class': 'form-control'}),
#         'sro_date': forms.DateInput(
#             attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Дата приёма в члены СРО”'}),
#         'sro_number': forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': 'Номер решения о приёме в члены СРО'}),
#         'license_date': forms.DateInput(
#             attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Дата прекращения членства”'}),
#         'url': forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': 'Сайт компании”'}),
#     }

# def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     legal_address_instance = self.instance.legal_address
#     self.fields['legal_address_postcode'].initial = legal_address_instance.postcode
#     self.fields['legal_address_city'].initial = legal_address_instance.city
#     self.fields['legal_address_street'].initial = legal_address_instance.street
#     self.fields['legal_address_house_number'].initial = legal_address_instance.house_number

#     # Получение выбранных типов работ для компании
#     self.fields['type_works'].initial = self.instance.specialization.values_list('type_work__pk', flat=True)

# def save(self, commit=True):
#     legal_address_instance = self.instance.legal_address
#     legal_address_instance.postcode = self.cleaned_data.get('legal_address_postcode')
#     legal_address_instance.city = self.cleaned_data.get('legal_address_city')
#     legal_address_instance.street = self.cleaned_data.get('legal_address_street')
#     legal_address_instance.house_number = self.cleaned_data.get('legal_address_house_number')
#     legal_address_instance.save()

#     # Сохранение связанных типов работ
#     type_works = self.cleaned_data.get('type_works')
#     self.instance.specialization.all().delete()  # Удаляем старые связи
#     for type_work in type_works:
#         CompanySpecialization.objects.create(type_work=type_work, company=self.instance)

#     return super().save(commit=commit)

# Форма создания адреса
class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = CompanyAddress
        fields = ['postcode', 'region', 'district', 'street', 'house_number']
        widgets = {field: forms.TextInput(attrs={'class': 'form-control'}) for field in fields[:-1]}
        widgets['region'] = forms.Select(attrs={'class': 'form-control'})


# Форма создания города
class CityCreateForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name', )
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


# Форма добавления директора филиала
class DirectorCreateForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ('position', 'surname', 'name', 'father_name')
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control'})
            for field in fields
        }


# Форма добавления сотрудника
class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('position', 'surname', 'name', 'father_name', 'phonenumber', 'email')
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control'})
            for field in fields
        }
