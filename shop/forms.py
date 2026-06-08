from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

FIELD_STYLE = (
    'width: 100%; padding: 12px 14px; border: 1px solid #d2d2d7; '
    'border-radius: 8px; font-size: 15px; font-family: inherit; '
    'color: #1d1d1f; background: #fff; transition: border-color 0.2s;'
)


class StyledUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['style'] = FIELD_STYLE


class CheckoutForm(forms.Form):
    address = forms.CharField(
        label='Адрес доставки',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Город, улица, дом, квартира...',
            'style': FIELD_STYLE,
        })
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '+375 (29) 123-45-67',
            'style': FIELD_STYLE,
        })
    )
    email = forms.EmailField(
        label='Email для получения чека',
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'style': FIELD_STYLE,
        })
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        clean_digits = ''.join(c for c in phone if c.isdigit())
        
        # Check if Belarusian format: starts with 375 (12 digits) or 80 (11 digits)
        if phone.startswith('+'):
            if not clean_digits.startswith('375') or len(clean_digits) != 12:
                raise forms.ValidationError("Введите корректный белорусский номер телефона (+375XXXXXXXXX).")
        else:
            if clean_digits.startswith('375'):
                if len(clean_digits) != 12:
                    raise forms.ValidationError("Введите корректный белорусский номер телефона (375XXXXXXXXX).")
            elif clean_digits.startswith('80'):
                if len(clean_digits) != 11:
                    raise forms.ValidationError("Введите корректный белорусский номер телефона (80XXXXXXXXX).")
            else:
                raise forms.ValidationError("Номер телефона должен быть белорусским (начинаться с +375 или 80).")
        return phone

    def clean_address(self):
        address = self.cleaned_data.get('address', '').strip()
        if len(address) < 10:
            raise forms.ValidationError("Пожалуйста, укажите адрес доставки более подробно (город, улица, дом, квартира).")
        if len(address) > 300:
            raise forms.ValidationError("Адрес не должен превышать 300 символов.")
        return address
