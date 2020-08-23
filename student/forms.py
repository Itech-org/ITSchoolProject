from django import forms
from django.contrib.auth.forms import AuthenticationForm
from manager_school.models import AdvUser
from django.contrib.auth.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = AdvUser
        fields = ('email', 'phone', 'img_user',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Логин *'},))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль *'}),)