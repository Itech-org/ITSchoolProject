from django import forms
from manager_school.models import AdvUser, Attendance, HomeworkTeacherModel


class UserEditForm(forms.ModelForm):
    class Meta:
        model = AdvUser
        fields = ('username', 'first_name', 'last_name', 'surname', 'email', 'phone', 'img_user',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
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

