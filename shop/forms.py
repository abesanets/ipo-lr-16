from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class StyledUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['style'] = (
                'width: 100%; padding: 10px; border: 1px solid #ddd; '
                'border-radius: 4px; font-size: 14px;'
            )


class CheckoutForm(forms.Form):
    """Форма оформления заказа"""
    address = forms.CharField(
        label='Адрес доставки',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Город, улица, дом, квартира...',
            'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;'
        })
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 123-45-67',
            'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;'
        })
    )
    email = forms.EmailField(
        label='Email для получения чека',
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;'
        })
    )