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
            'placeholder': '+7 (999) 123-45-67',
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
