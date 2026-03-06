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