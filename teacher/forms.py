from django import forms
from manager_school.models import AdvUser, Attendance, HomeworkTeacherModel


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
