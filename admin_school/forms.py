from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import Select
from django.contrib.auth.forms import AuthenticationForm
from manager_school.models import ClassModel
from manager_school.models import News
from manager_school.models import RubruckNews
from manager_school.models import Costs



class ClassModelForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'main__schedule-input'}))
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'main__schedule-input','placeholder':"Укажите причину переноса"}))
    # classroom = forms.CharField(widget=forms.TextInput(attrs={'class': ''}))

    class Meta:
        model = ClassModel
        fields = ('classroom',
                  'date',
                  'message')


class CostsForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'td__color_dark', 'type': 'date' }))
    breakdown = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'td__color_dark'}), required=False)
    chancery = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'td__color_dark'}), required=False)
    grocery = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'td__color_dark'}), required=False)
    house_chemicals = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'td__color_dark'}), required=False)
    total = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'td__color_dark'}))

    class Meta:
        model = Costs
        fields = ('date', 'breakdown', 'chancery',
                  'grocery', 'house_chemicals',
                  'total')


class NewsForm(forms.ModelForm):
    description = forms.CharField(label='Новостная статья', widget=CKEditorWidget())


    class Meta:
        model = News
        fields = ("title", "rubrick", 'description')


class RubrickForm(forms.ModelForm):

    class Meta:
        model = RubruckNews
        fields = ("title",)
        widgets = {"rubrick": Select(attrs={'size': 4})}


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'main__open-student-input', 'placeholder': 'Логин *'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'main__open-student-input', 'placeholder': 'Пароль *'}))

