from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView, LogoutView

from django.db.models import Q
from django.shortcuts import render

from django.urls import reverse_lazy

from manager_school.utilities import user_passes_test_custom
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpRequest, HttpResponse
from manager_school.models import *
from django.contrib import messages
from .forms import UserEditForm, AttendanceEdit, HwTeacherEdit
import calendar
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.


class Login_View(LoginView): #вход
    template_name = 'teacher/login.html'

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        print(form)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Logout_View(LoginRequiredMixin, LogoutView): #выход
    template_name = "teacher/logout.html"


def check_group_and_activation(request): #авторизация
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Teacher").exists():
            return True
        else:
            logout(request)
            return False
    else:
        return False


@user_passes_test_custom(check_group_and_activation, login_url='login/') #главная
def index(request):
    return render(request, 'teacher/index.html')


@user_passes_test_custom(check_group_and_activation, login_url='login/')
def calendar(request): #календарь
    cl=[]
    groups = GroupModel.objects.filter(teacher__id=request.user.id)
    for i in groups:
        classes = ClassModel.objects.filter(groups_id=i.id)
        cl+=classes
    context={'classes':cl}
    print(context)
    return render(request, 'teacher/calendar.html', context)


def profile(request): #страница профиля учителя
    return render(request, 'teacher/profile.html')



def account(request): #профиль
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Ваши данные успешно изменены')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'teacher/account.html', {'user_form': user_form})



@user_passes_test_custom(check_group_and_activation, login_url='login/')
def group_detail(request):
    groups = GroupModel.objects.filter(teacher__id=request.user.id)
    return render(request, "teacher/group_detail.html", {'groups':groups})


@user_passes_test_custom(check_group_and_activation, login_url='login/')
def study_procces(request):
    return render(request, 'teacher/study_procces.html')


@user_passes_test_custom(check_group_and_activation, login_url='login/')
def my_courses(request):
    my_id = request.user.id
    group = get_object_or_404(GroupModel, students__id = my_id)
    courses = group.course.all()
    context = {'courses':courses}
    return render(request, "student/my_courses.html", context)


@user_passes_test_custom(check_group_and_activation, login_url='login/')
def exact_course(request, course_id):
    course = get_object_or_404(CourseModel, id = course_id)
    context = {'course':course}
    return render(request, "student/exact_course.html", context)


@user_passes_test_custom(check_group_and_activation, login_url='login/')
def homework_view(request):
    context = {'homework':homework}
    return render(request, "teacher/homework.html", context)


@user_passes_test_custom(check_group_and_activation, login_url='login')
def shedule_view(request):
    my_id = request.user.id
    group = get_object_or_404(GroupModel, students__id = my_id)
    group_id = group.id
    shedule = get_object_or_404(SheduleModel, group__id = group_id)
    shedule_id = shedule.id
    cls = get_list_or_404(ClassModel, timetable__id = shedule_id)
    context = {'shedule':shedule, 'class':cls}
    return render(request, "student/shedule.html", context)


@user_passes_test_custom(check_group_and_activation, login_url='login')
def class_view(request, class_id):
    cls = get_object_or_404(ClassModel, id = class_id)
    material = get_object_or_404(MaterialModel, class_field__id = class_id)
    homework = get_object_or_404(HomeworkModel, class_field__id = class_id)
    context = {'class': cls, 'material':material, 'homework':homework}
    return render(request, "student/class.html", context)



class MyPasswordChange(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    """ Смена пароля """
    template_name = 'teacher/password_change.html'
    success_url = reverse_lazy('teacher:password')
    success_message = 'Ваш пароль успешно изменён'


class MyPasswordReset(PasswordResetView):
    success_url = reverse_lazy('teacher:password_reset_done')


class MyPasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('teacher:password_reset_complete')


def group_detail(request): #вкладка группы
    context={'students': ''}
    filter_gr=request.GET.get('choise','')
    if filter_gr:
        students = AdvUser.objects.filter(groupmodel=filter_gr)
        context.update({'students': students})
        print(context)
    else:
        context
    return render(request, "teacher/group_detail.html", context)


def study_procces(request): #учебный процесс
    return render(request, 'teacher/study_procces.html')


def student_detail(request, student_id): #детализация ученика
    student = get_object_or_404(AdvUser, id=student_id)
    return render(request, 'teacher/student_detail.html', {'student':student})


def materials(request): #материалы
    return render(request, 'teacher/materials.html')


def text_mat(request): #список книг
    search_q = request.GET.get('search', '')
    if search_q:
        literature = MaterialText.objects.filter(title__icontains=search_q)
    else:
        literature = MaterialText.objects.all()
    return render(request, 'teacher/text_mat.html', {'literature':literature})


def text_detail(request, slug_l): #страница книги
    literature = MaterialText.objects.filter(slug=slug_l)
    return render(request, 'teacher/text_detail.html', {'literature':literature})


def video_mat(request): #список видео
    search_q = request.GET.get('search','')
    if search_q:
        videos = MaterialVideo.objects.filter(Q(title__icontains=search_q) | Q(description__icontains=search_q))
    else:
        videos = MaterialVideo.objects.all()
    return render(request, 'teacher/video_mat.html', {'videos':videos})


def video_detail(request, slug_v): #станица видео
    video = MaterialVideo.objects.filter(slug=slug_v)
    return render(request, 'teacher/video_detail.html', {'video':video})


# def class_detail(request, class_id): #страница занятия
#     cls = get_object_or_404(ClassModel, id=class_id)
#     group = get_object_or_404(GroupModel, classes=class_id)
#     course = get_object_or_404(CourseUser, groups=group.id)
#     students = AdvUser.objects.filter(groupmodel=group.id)
#     if request.method == 'POST':
#         # form_at = AttendanceEdit(request.POST)
#         form_hw = HwTeacherEdit(request.POST)
#         if form_at.is_valid() and form_hw.is_valid():
#             form_at.save()
#             form_hw.save()
#             return render(request, 'teacher/success.html')
#     else:
#         form_at = AttendanceEdit()
#         form_hw = HwTeacherEdit()
#     context = {'group':group, 'class':cls, 'course':course, 'form_at':form_at, 'form_hw':form_hw, 'students':students}
#     print(context)
#     return render(request, 'teacher/class_detail.html', context)


def homework(request): #дз студентов
    homework=[]
    context = {'homework': ''}
    filter_gr = request.GET.get('choise', '')
    if filter_gr:
        students = AdvUser.objects.filter(groupmodel=filter_gr)
        for st in students:
            homework += st.homework_st.all()
        context['homework'] = homework
        print(context)
    else:
        context
    return render(request, 'teacher/homework.html', context)


def homework_detail(request, hw_id): #страница дз студента
    return render(request, 'teacher/homework_detail.html')


def materials_on_theme(request): #материалы по темам
    return render(request, 'teacher/materials_on_theme.html')


def material_detail(request): #страница материала
    return render(request, 'teacher/material_detail.html')


def video_courses(request): #видеозанития
    return render(request, 'teacher/video_courses.html')


def vd_crs_detail(request): #страница видеозанятия
    return render(request, 'teacher/vd_crs_detail.html')


def chat(request): #чат
    return render(request, 'teacher/chat.html')


def teachers(request): #преподаватели
    return render(request, 'teacher/teachers.html')


def news(request): #новости
    return render(request, 'teacher/news.html')

