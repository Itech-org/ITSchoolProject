from django import forms
from manager_school.models import AdvUser
from django.contrib.auth.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = AdvUser
        fields = ('email', 'phone', 'img_user',)
