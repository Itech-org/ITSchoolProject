import django_filters
from django_filters import DateTimeFromToRangeFilter
from django_filters.widgets import RangeWidget
from .models import StudyRequest, AdvUser, GroupModel, CourseUser
from django.forms import widgets


class StudyRequestFilter(django_filters.FilterSet):
    SPECIALIST_CHOICES = [(m.id, m.last_name + m.first_name) for m in AdvUser.objects.filter(groups__name='Manager')]
    STATUS_CHOICES = (
        ('Ready', 'Ready'),
        ('In Progress', 'In Progress'),
        ('Denial', 'Denial'),
    )
    enter_date = DateTimeFromToRangeFilter(widget=RangeWidget(attrs={'class': 'form-control mb-2', 'placeholder': 'dd.mm.yyyy'}))
    specialist = django_filters.ChoiceFilter(choices=SPECIALIST_CHOICES, widget=widgets.Select(attrs = {'class': 'form-control mb-2', 'placeholder': 'Специалист'}))
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES, widget=widgets.Select(attrs = {'class': 'form-control mb-2', 'placeholder': 'Статус'}))
    class Meta:
        model = StudyRequest
        fields = ['enter_date', 'specialist', "status"]


class GroupFilter(django_filters.FilterSet):
    COURSE_CHOICES = [(c.id, c.title) for c in CourseUser.objects.all()]
    TEACHER_CHOICES = [(m.id, m.last_name + m.first_name) for m in AdvUser.objects.filter(groups__name='Teacher')]
    MANAGER_CHOICES = [(m.id, m.last_name + m.first_name) for m in AdvUser.objects.filter(groups__name='Manager')]

    course = django_filters.ChoiceFilter(choices=COURSE_CHOICES, widget=widgets.Select(attrs = {'class': 'form-control mb-2'}))
    teacher = django_filters.ChoiceFilter(choices=TEACHER_CHOICES, widget=widgets.Select(attrs = {'class': 'form-control mb-2'}))
    manager = django_filters.ChoiceFilter(choices=MANAGER_CHOICES, widget=widgets.Select(attrs = {'class': 'form-control mb-2'}))
    class Meta:
        model = GroupModel
        fields = ['teacher', 'manager',  'course']
