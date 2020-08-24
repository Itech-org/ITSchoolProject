from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.forms import Select
from manager_school.models import ClassModel
from manager_school.models import News
from manager_school.models import RubruckNews


class ClassModelForm(forms.ModelForm):

    class Meta:
        model = ClassModel
        fields = ('classroom', 'date')


class NewsForm(forms.ModelForm):
    description = forms.CharField(label='Новостная статья', widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = ("title", "description", "rubrick")


class RubrickForm(forms.ModelForm):

    class Meta:
        model = RubruckNews
        fields = ("title",)