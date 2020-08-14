from django import forms
from manager_school.models import ClassModel


class ClassModelForm(forms.ModelForm):

    class Meta:
        model = ClassModel
        fields = ('classroom', 'date')