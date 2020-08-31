from django.contrib.auth.forms import AuthenticationForm

from .models import *
from django import forms
from django.contrib.auth.models import Group


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


class RegistrationForm(forms.ModelForm):
    group_user = forms.ModelChoiceField(empty_label='Выберите группу', queryset=Group.objects.all(), widget=forms.Select(attrs={'class': 'main__student-card-info-input'}))

    def save(self, commit=True):
        password = AdvUser.objects.make_random_password()
        print(password)
        user = super().save(commit=False)
        user.set_password(password)
        user.is_active = True
        user.is_activated = True

        if commit:
            user.save()
        user.groups.add(Group.objects.get(name=self.cleaned_data['group_user']))
        # send_password(user, password)
        with open('passwords.txt', 'a') as f:
            f.write(f'Login: {user.username}. Password: {password}\n')
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'last_name', 'first_name', 'surname', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'main__student-card-info-input'}),
            'email': forms.EmailInput(attrs={'class': 'main__student-card-info-input'}),
            'last_name': forms.TextInput(attrs={'class': 'main__student-card-info-input'}),
            'first_name': forms.TextInput(attrs={'class': 'main__student-card-info-input'}),
            'surname': forms.TextInput(attrs={'class': 'main__student-card-info-input'}),
            'phone': forms.TextInput(attrs={'class': 'main__student-card-info-input'}),
        }


class RequestConversationForm(forms.ModelForm):
    CHOICES = (
        ('Ready', 'Ready'),
        ('Сall back', 'Сall back'),
        ('Denial', 'Denial'),
    )
    date = forms.DateTimeField(required=False, label='Дата',
                               widget=forms.DateTimeInput(attrs={"type": "date"}))
    theses_of_conversation = forms.CharField(required=False, label='Тезисы разговора',
                                             widget=forms.Textarea(attrs={}))
    status = forms.ChoiceField(label='Статус разговора', choices=CHOICES,
                               widget=forms.Select(attrs={}))

    class Meta:
        model = RequestConversation
        fields = ('date', 'status', 'theses_of_conversation', 'request')


class StudyRequestForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('Ready', 'Ready'),
        ('In Progress', 'In Progress'),
        ('Denial', 'Denial'),
    )

    enter_date = forms.DateTimeField(label='Дата', widget=forms.DateTimeInput(attrs={"type": "date"}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={}))
    patronymic = forms.CharField(label='Отчество',
                                 widget=forms.TextInput(attrs={}))
    communication_type = forms.CharField(label='Способ связи',
                                         widget=forms.TextInput(attrs={}))
    tel_number = forms.CharField(label='Телефон',
                                         widget=forms.TextInput(attrs={}))
    email = forms.EmailField(label='E-mail',
                                 widget=forms.EmailInput(attrs={}))
    source = forms.CharField(label='Источник', widget=forms.TextInput(attrs={}))
    course = forms.ModelChoiceField(label='Курс', queryset=CourseUser.objects.all(),
                                    widget=forms.Select(attrs={}))
    status = forms.ChoiceField(label='Статус разговора', choices=STATUS_CHOICES,
                               widget=forms.Select(attrs={}))
    specialist = forms.ModelChoiceField(label='Менеджер', queryset=AdvUser.objects.filter(groups__name='Manager'),
                                        widget=forms.Select(attrs={}))



    class Meta:
        model = StudyRequest
        fields = ('enter_date', 'last_name', 'first_name', 'patronymic', 'communication_type',
                  'tel_number', 'email', 'course', 'source', 'specialist', 'status',)


class ContractForm(forms.ModelForm):
    number = forms.CharField(label='Номер', widget=forms.TextInput(attrs={"placeholder": "Номер договора"}))
    date = forms.DateField(label='Дата заключения', initial='Выберите дату',
                           widget=forms.TextInput(attrs={"type": "date"}))
    course = forms.ModelChoiceField(label='Курс', queryset=CourseUser.objects.all(), initial='Выберите курс',
                                    widget=forms.Select())
    group = forms.ModelChoiceField(label='Группа', queryset=GroupModel.objects.all(), initial='Выберите группу',
                                   widget=forms.Select())
    account = forms.ModelChoiceField(label='Аккаунт', queryset=AdvUser.objects.filter(groups__name='Student'),
                                     initial='Выберите аккаунт', widget=forms.Select())
    price = forms.CharField(label='Цена', widget=forms.TextInput(attrs={'placeholder': 'Цена'}))

    lead = forms.IntegerField(widget=forms.HiddenInput(), label='')

    class Meta:
        model = Contract
        fields = ('number', 'date', 'course', 'group', 'account', 'price', 'lead')


class PaymentStageForm(forms.ModelForm):
    price = forms.CharField(label='Цена', widget=forms.TextInput(attrs={'placeholder': 'Цена платежа'}))
    date = forms.DateField(label='Дата этапа оплаты',
                           widget=forms.DateTimeInput(attrs={'type': 'date'}))
    class Meta:
        model = PaymentStage
        fields = ('picture', 'price', 'date', 'payment', 'is_confirmed')


class GroupModelForm(forms.ModelForm):

    title = forms.CharField(label='Название группы', widget=forms.TextInput(attrs={}))
    course = forms.ModelChoiceField(label='Курс', queryset=CourseUser.objects.all(),
                                    widget=forms.Select(attrs={}))
    manager = forms.ModelChoiceField(label='Куратор', queryset=AdvUser.objects.filter(groups__name='Manager'),
                                        widget=forms.Select(attrs={}))
    teacher = forms.ModelChoiceField(label='Преподаватель', queryset=AdvUser.objects.filter(groups__name='Teacher'),
                                     widget=forms.Select(attrs={}))
    class Meta:
        model = GroupModel
        fields = ('manager', 'teacher', 'course', 'title')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message', 'document']
        labels = {'message': ""}
        widgets = {
            'message': forms.Textarea(attrs={'class': 'main__chat-textarea', 'cols': '30', 'rows': '10', 'placeholder': 'Введите текст'}),
            'document': forms.FileInput(attrs={'class': 'main__chat-message-input-file'})
        }