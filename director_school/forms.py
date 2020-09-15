from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'placeholder': 'Логин *',
        'class': 'main__open-student-input',
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль *',
        'class': 'main__open-student-input',
    }))
    remember_me = forms.BooleanField(required=False, label='Запомнить меня?',
                                     widget=forms.CheckboxInput(attrs={'id': 'squaredThree'}))