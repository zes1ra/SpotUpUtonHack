from django import forms
from .models import UserCustom


class UserRegistrationForm(forms.ModelForm):
    password_check = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    email = forms.EmailField(label='Адрес электронной почты', help_text='user@mail.com')

    class Meta:
        model = UserCustom
        fields = [
            'username',
            'email',
            'phone',
            'password',
            'password_check',
        ]

    # def __init__(self, *args, **kwargs):
    #     super(RegistrationForm, self).__init__(*args, **kwargs)
    #     self.fields['email'].help_text = 'user@mail.com'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserCustom
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'phone',
            'country',
            'city',
            'street',
            'index',
            'info'
        ]
