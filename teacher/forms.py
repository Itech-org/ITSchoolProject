from django import forms
from django.contrib.auth.forms import AuthenticationForm
from manager_school.models import AdvUser, Attendance, HomeworkTeacherModel, Message


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':"main__open-student-input" ,'placeholder': 'Логин *'},))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':"main__open-student-input" ,'placeholder': 'Пароль *'}),)



class UserEditForm(forms.ModelForm):
    class Meta:
        model = AdvUser
        fields = ('email', 'phone',)
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'change-personal-data__change-data',}),
            'email': forms.TextInput(attrs={'class': 'change-personal-data__change-data',}),
            }

class AttendanceEdit(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('classes', 'students','rating', 'attendance')
        widgets = {
            'classes': forms.Select(),
            'students': forms.Select(),
            'rating': forms.NumberInput(),
            'attendance': forms.CheckboxInput(),
            }


class HwTeacherEdit(forms.ModelForm):
    class Meta:
        model = HomeworkTeacherModel
        fields = {'title', 'description','class_field', 'file', 'url',}
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'class_field': forms.Select(),
            'file': forms.FileInput(),
            'url': forms.URLInput(),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message', 'document']
        labels = {'message': ""}
        widgets = {
            'message': forms.Textarea(attrs={'class': 'main__chat-textarea', 'cols': '30', 'rows': '10', 'placeholder': 'Введите текст'}),
            'document': forms.FileInput(attrs={'class': 'main__chat-message-input-file'})
        }
