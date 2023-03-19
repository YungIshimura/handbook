from django import forms
# from .validators import validate_cadastral_number
from .models import TypeWork, Order
from django.core.validators import MinValueValidator


class OrderForm(forms.ModelForm):
    cadastral_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Кадастровый номер'}))
    street = forms.CharField()
    house_number = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'class':'border mr-2 application--form--input-group__house'})
    )
    building = forms.IntegerField(
        validators=[MinValueValidator(1)]
    )
    square = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Ширина'})
    )
    length = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Длина'})
    )
    width = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': ' Ширина'})
    )
    heigth = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Высота'})
    )
    type_work = forms.ModelChoiceField(
        queryset=TypeWork.objects.all(), 
        widget=forms.RadioSelect()
    )
    title = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Название объекта'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'})
    )
    surname = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия'})
    )
    father_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваше отчество'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона'})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите номер телефона'}))

    class Meta:
        model = Order
        fields = ('cadastral_number', 'region', 'area', 'city', 'street', 'house_number', 'building',
                  'square', 'length', 'width', 'heigth', 'title', 'name', 'type_work', 'surname', 'father_name', 'phone_number', 'email')
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'application--form__data-input border'
        self.fields['house_number'].widget.attrs['class'] = 'border mr-2 application--form--input-group__house'
        self.fields['building'].widget.attrs['class'] = 'border application--form--input-group__house'
    
        self.fields['square'].widget.attrs['class'] = 'form-control data-inputdimensions'
        self.fields['length'].widget.attrs['class'] = 'form-control'
        self.fields['heigth'].widget.attrs['class'] = 'form-control'
        self.fields['width'].widget.attrs['class'] = 'form-control'

        self.fields['title'].widget.attrs['class'] = 'application--form--textarea__text form-control'
        self.fields['title'].widget.attrs['style'] = 'margin-top:20px;'

        self.fields['name'].widget.attrs['class'] = 'form-control application--form__data-input'
        self.fields['surname'].widget.attrs['class'] = 'form-control application--form__data-input'
        self.fields['father_name'].widget.attrs['class'] = 'form-control application--form__data-input'

        self.fields['phone_number'].widget.attrs['class'] = 'form-control application--form__data-input'
        self.fields['email'].widget.attrs['class'] = 'form-control application--form__data-input'