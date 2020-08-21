from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView, LogoutView

from django.db.models import Q
from .serializers import ClassModelSerializer
from django.urls import reverse_lazy
import datetime
from manager_school.utilities import user_passes_test_custom
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.http import HttpRequest, HttpResponse
from manager_school.models import *
from django.contrib import messages
from .forms import UserEditForm, AttendanceEdit, HwTeacherEdit
import calendar
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from rest_framework.decorators import api_view
from rest_framework.response import Response

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


@user_passes_test_custom(check_group_and_activation, login_url='teacher/login/')
def calendar(request):
    classes = {}
    group = request.GET.get('group', '')
    if group:
        classes = ClassModel.objects.filter(groups=group)
    else:
        {'classes':''}
    date_now = datetime.datetime.now()
    print(classes)
    return render(request, 'teacher/calendar.html', {'classes':classes, 'date_now':date_now})


@user_passes_test_custom(check_group_and_activation, login_url='/teacher/login/')
def class_detail(request, class_id):
    class_data = get_object_or_404(ClassModel, id=class_id)
    attendances = Attendance.objects.filter(classes__id=class_id)
    return render(request, "teacher/calendar-go-to-day.html", {
        "class": class_data,
        "attendances": attendances,
    })

@api_view(['GET']) #api_calendar
def api_classes_list(request):
    group = request.GET.get('group', '')
    if group == '':
        classes = ClassModel.objects.all()
    else:
        try:
            selected_group = int(group)
            classes = ClassModel.objects.filter(groups__id=selected_group)
        except TypeError:
            classes = ClassModel.objects.all()
    data = ClassModelSerializer(classes, many=True)
    return Response(data.data)


def profile(request): #страница профиля учителя
    groups = GroupModel.objects.filter(teacher__id=request.user.id)
    classes = 0
    for g in groups:
        classes += int(g.course.amount)
    return render(request, 'teacher/card_personal_teacher.html', {'classes':classes})



def profile_edit(request): #редактирование профиля
    if request.method == "POST":
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        img_user = request.FILES.get('img_user', '')
        user = request.user
        if phone:
            user.phone = phone
        elif email:
            user.email = email
        elif img_user:
            user.img_user = img_user
        user.save()
        return redirect('teacher:profile')
    # if request.method == 'POST':
    #     user_form = UserEditForm(instance=request.user, data=request.POST)
    #     if user_form.is_valid():
    #         user_form.save()
    #         messages.success(request, 'Ваши данные успешно изменены')
    # else:
    #     user_form = UserEditForm(instance=request.user)
    return render(request, 'teacher/change_personal_data.html')


@user_passes_test_custom(check_group_and_activation, login_url='login/')
def study_procces(request):
    return render(request, 'teacher/studying_proccess.html')


class MyPasswordChange(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    """ Смена пароля """
    template_name = 'teacher/password_change.html'
    success_url = reverse_lazy('teacher:password')
    success_message = 'Ваш пароль успешно изменён'


class MyPasswordReset(PasswordResetView):
    success_url = reverse_lazy('teacher:password_reset_done')


class MyPasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('teacher:password_reset_complete')


@user_passes_test_custom(check_group_and_activation, login_url='teacher/login/')
def group_detail(request): #вкладка группы
    students=[]
    filter_gr=request.GET.get('group','')
    if filter_gr:
        students = AdvUser.objects.filter(groupmodel=filter_gr)
        print(students)
    else:
        groups = GroupModel.objects.filter(teacher__id=request.user.id)
        for g in groups:
            students += AdvUser.objects.filter(groupmodel=g.id)
    return render(request, "teacher/group.html", {'students':students})


def student_detail(request, student_id): #детализация ученика
    student = get_object_or_404(AdvUser, id=student_id)
    return render(request, 'teacher/student_detail.html', {'student':student})


def materials(request): #материалы
    return render(request, 'teacher/studying_materials.html')


def text_mat(request): #список книг
    search_q = request.GET.get('search', '')
    if search_q:
        literature = MaterialText.objects.filter(title__icontains=search_q)
    else:
        literature = MaterialText.objects.all()
    return render(request, 'teacher/education-literature.html', {'literature':literature})


def text_detail(request, slug_l): #страница книги
    literature = MaterialText.objects.filter(slug=slug_l)
    return render(request, 'teacher/text_detail.html', {'literature':literature})


def video_mat(request): #список видео
    search_q = request.GET.get('search','')
    if search_q:
        videos = MaterialVideo.objects.filter(Q(title__icontains=search_q) | Q(description__icontains=search_q))
    else:
        videos = MaterialVideo.objects.all()
    return render(request, 'teacher/video-material.html', {'videos':videos})


def video_detail(request, slug_v): #станица видео
    video = MaterialVideo.objects.filter(slug=slug_v)
    return render(request, 'teacher/video_detail.html', {'video':video})

def homework(request): #дз студентов
    homework=[]
    students = []
    filter_gr=request.GET.get('group','')
    if filter_gr:
        students = AdvUser.objects.filter(groupmodel=filter_gr)
        for st in students:
            homework += st.homework_st.all()
    else:
        groups = GroupModel.objects.filter(teacher__id=request.user.id)
        for g in groups:
            students += AdvUser.objects.filter(groupmodel=g.id)
        print(students)
        for st in students:
            homework += st.homework_st.all()
    return render(request, 'teacher/students-homework.html', {'homework':homework})


def homework_detail(request, hw_id): #страница дз студента
    hw = get_object_or_404(HomeworkModel, id=hw_id)
    student = hw.user
    return render(request, 'teacher/choosing-dz.html', {'student':student, 'homework':hw})


def materials_on_theme(request): #материалы по темам
    return render(request, 'teacher/materials_on_topics.html')


def material_detail(request): #страница материала
    return render(request, 'teacher/material_detail.html')


def video_courses(request): #видеозанития
    return render(request, 'teacher/video-material.html')


def vd_crs_detail(request): #страница видеозанятия
    return render(request, 'teacher/vd_crs_detail.html')


def chat(request): #чат
    return render(request, 'teacher/chat.html')


def teachers(request): #преподаватели
    teachers = AdvUser.objects.filter(groups__name='Teacher')
    return render(request, 'teacher/teachers.html', {'teachers':teachers})


def news(request): #новости
    news = News.objects.all()
    return render(request, 'teacher/itnews.html', {'news':news})


def post_detail(request, post_id):
    post = get_object_or_404(News, id=post_id)
    return render(request, 'teacher/container_news.html', {'post':post})


def message_for_admin(request):
    return render(request, 'teacher/contact_administrator.html')
