from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.db.models import Q, Count
from .serializers import ClassModelSerializer
from django.urls import reverse_lazy
import datetime

from django.utils.text import slugify
from manager_school.utilities import user_passes_test_custom
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.http import HttpRequest, HttpResponse
from manager_school.models import *
from django.contrib import messages
from .forms import UserEditForm, AttendanceEdit, HwTeacherEdit, MessageForm, LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    return redirect("teacher:login")
                else:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    return redirect('teacher:index')
            else:
                return redirect("teacher:login")
        else:
            form = LoginForm()
            return render(request, 'teacher/login.html', {'form': form})
    else:
        return redirect('teacher:index')


@login_required
def logout_request(request):
    logout(request)
    return redirect("entry_page")


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


# ------------------------------- КАЛЕНДАРЬ -----------------------------------


@user_passes_test_custom(check_group_and_activation, login_url='teacher/login/')
def calendar(request):
    classes = []
    group = request.GET.get('group', '')
    if group:
        classes = ClassModel.objects.filter(groups=group).filter(date__gte=datetime.datetime.now())
    else:
        groups = GroupModel.objects.filter(teacher__id=request.user.id)
        for g in groups:
            classes += g.classes.all().filter(date__gte=datetime.datetime.now())
    date_now = datetime.datetime.now()
    print(classes)
    return render(request, 'teacher/calendar.html', {'classes':classes, 'date_now':date_now})


@api_view(['GET']) #api_calendar
def api_classes_list(request):
    classes =[]
    group = request.GET.get('group', '')
    if group == '':
        groups = GroupModel.objects.filter(teacher__id=request.user.id)
        for g in groups:
            classes += g.classes.all()
    else:
        try:
            selected_group = int(group)
            classes = ClassModel.objects.filter(groups__id=selected_group)
        except TypeError:
            groups = GroupModel.objects.filter(teacher__id=request.user.id)
            for g in groups:
                classes += g.classes.all()
    data = ClassModelSerializer(classes, many=True)
    return Response(data.data)


# -------------------------------- ЗАНЯТИЕ -------------------------------------


@user_passes_test_custom(check_group_and_activation, login_url='/teacher/login/')
def class_detail(request, class_id):
    class_data = get_object_or_404(ClassModel, id=class_id)
    attendances = Attendance.objects.filter(classes__id=class_id)
    literature = MaterialText.objects.all()
    video = MaterialVideo.objects.all()
    if request.method == 'POST':
        #тема занятия
        theme = request.POST.get('theme', '')
        if theme:
            class_data.theme = theme
            class_data.save()
        #дз препода
        if request.POST.get('file', ''):
            file_t = request.POST['file']
        else:
            file_t = None
        hw_t = HomeworkTeacherModel.objects.create(class_field=class_data,
            title=request.POST.get('title', ''),
            description = request.POST.get('description', ''),
            url = request.POST.get('url', ''),
            file=file_t,
            slug=slugify(request.POST.get('title', ''))
            )
        hw_t.save()
        #посещение
        for st in class_data.groups.students.all():
            status = request.POST.get('status-{}'.format(st.id), '')
            rating = request.POST.get('rating-{}'.format(st.id), '')
            att = Attendance.objects.create(students=st, classes=class_data, rating=int(rating), attendance=status)
            att.save()
        return redirect('teacher:calendar')
    return render(request, "teacher/calendar-go-to-day.html", {
        "class": class_data,
        "attendances": attendances,
        'literature':literature,
        'video':video})


# ----------------------------- ДЗ СТУДЕНТОВ -----------------------------------


def homework(request): #дз студентов
    homework=[]
    students = []
    filter_gr=request.GET.get('group','')
    filter_date=request.GET.get('date','')
    filter_status=request.GET.get('status','')
    if filter_gr:
        students = AdvUser.objects.filter(groupmodel=filter_gr)
        for st in students:
            homework += st.homework_st.all()
    else:
        groups = GroupModel.objects.filter(teacher__id=request.user.id)
        for g in groups:
            students += AdvUser.objects.filter(groupmodel=g.id)
        for st in students:
            homework += st.homework_st.all()
    return render(request, 'teacher/students-homework.html', {'homework':homework})


def homework_detail(request, hw_id): #страница дз студента
    hw = get_object_or_404(HomeworkModel, id=hw_id)
    student = hw.user
    comment_file = hw.comment_file
    if request.method == 'POST':
        print(request.POST)
        cmt_tx = request.POST.get('autor_text', '')
        if request.FILES.get('comment_file', ''):
            comment_file = request.FILES['comment_file']
        st = request.POST.get('status', '')
        rating = request.POST.get('rating', '')
        if rating:
            hw.rating = rating
        if cmt_tx:
            hw.comment_teacher = cmt_tx
        if comment_file:
            hw.comment_file = comment_file
        if st:
            hw.status = st
        hw.save()
        return redirect('teacher:homework')
    return render(request, 'teacher/choosing-dz.html', {'student':student, 'homework':hw})


# -------------------------------- ПРОФИЛЬ-----------------------------------


def profile(request): #страница профиля учителя
    groups = GroupModel.objects.filter(teacher__id=request.user.id)
    classes = 0
    for g in groups:
        classes += int(g.course.amount)
    return render(request, 'teacher/card_personal_teacher.html', {'classes':classes})



def profile_edit(request): #редактирование профиля
    user = request.user
    if request.method == "POST":
        user.img_user = request.user.img_user
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        if request.POST.get('img_user', ''):
            img_user = request.FILES['img_user']
        if phone:
            user.phone = phone
        if email:
            user.email = email
        user.save()
        return redirect('teacher:profile')
    return render(request, 'teacher/change_personal_data.html')


class MyPasswordChange(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    """ Смена пароля """
    template_name = 'teacher/password_change.html'
    success_url = reverse_lazy('teacher:password')
    success_message = 'Ваш пароль успешно изменён'


class MyPasswordReset(PasswordResetView):
    success_url = reverse_lazy('teacher:password_reset_done')


class MyPasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('teacher:password_reset_complete')


# ---------------------------- УЧЕБНЫЙ ПРОЦЕСС ---------------------------------


@user_passes_test_custom(check_group_and_activation, login_url='login/')
def study_procces(request):
    return render(request, 'teacher/studying_proccess.html')


# --------------------------------- ГРУППЫ ------------------------------------


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
    attendance = Attendance.objects.filter(students__id=student.id)
    return render(request, 'teacher/students_personal_card.html', {'student': student, 'attendance': attendance})


# ------------------------------ МАТЕРИАЛЫ ---------------------------------


def materials(request): #материалы
    return render(request, 'teacher/studying_materials.html')


# ------------------------------ ЛИТЕРАТУРА -----------------------------------


def text_mat(request): #список книг
    search_q = request.GET.get('search', '')
    if search_q:
        literature = MaterialText.objects.filter(title__icontains=search_q)
    else:
        literature = MaterialText.objects.all()
    return render(request, 'teacher/education-literature.html', {'literature':literature})


def text_detail(request, l_id): #страница книги
    literature = get_object_or_404(MaterialText, id=l_id)
    return render(request, 'teacher/literature_literature.html', {'literature':literature})


# ---------------------------- ВИДЕОМАТЕРИАЛЫ ----------------------------------


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


# ---------------------------- МАТ ПО ТЕМАМ -----------------------------------


def materials_on_theme(request): #материалы по темам
    classes = []
    group = request.GET.get('group', '')
    if group:
        classes = ClassModel.objects.filter(groups=group)
    else:
        groups = GroupModel.objects.filter(teacher__id=request.user.id)
        for g in groups:
            classes += g.classes.all()
    date_now = datetime.datetime.now()
    print(classes)
    return render(request, 'teacher/materials_on_topics.html', {'classes':classes, 'date_now':date_now})


def material_detail(request, class_id): #страница материала
    class_data = get_object_or_404(ClassModel, id=class_id)
    return render(request, 'teacher/selected-lesson.html', {'class':class_data})


# ---------------------------- ВИДЕО ЗАНЯТИЙ ----------------------------------


def video_courses(request): #видеозанития
    return render(request, 'teacher/video-material.html')


def vd_crs_detail(request): #страница видеозанятия
    return render(request, 'teacher/vd_crs_detail.html')



# ----------------------------- ПРЕПОДАВТЕЛИ ----------------------------------


def teachers(request): #преподаватели
    teachers = AdvUser.objects.filter(groups__name='Teacher')
    return render(request, 'teacher/teachers.html', {'teachers':teachers})


def teacher_card(request, t_id):
    teacher = get_object_or_404(AdvUser, id=t_id)
    return render(request, 'teacher/teacher_card.html', {'teacher':teacher})


# --------------------------------- НОВОСТИ ------------------------------------


def news(request): #новости
    news = News.objects.all()
    return render(request, 'teacher/itnews.html', {'news':news})


def post_detail(request, post_id):
    post = get_object_or_404(News, id=post_id)
    return render(request, 'teacher/container_news.html', {'post':post})


# ---------------------- СООБЩЕНИЕ ДЛЯ АДМИНИСТРАТОРА --------------------------


@user_passes_test_custom(check_group_and_activation, login_url='teacher/login')
def message_for_admin(request):
    if request.method == "POST":
        print(request.POST)
        admin = AdvUser.objects.filter(groups__name="Admin").order_by('-last_login')[0]
        chats = Chat.objects.filter(members__in=[request.user.id, admin.id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(admin.id)
        else:
            chat = chats.first()
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat.id
            message.author = request.user
            message.save()
        return redirect(reverse('teacher:messages', kwargs={'chat_id': chat.id}))
    return render(request, 'teacher/contact_administrator.html')


# ----------------------------------- ЧАТ -------------------------------------


@user_passes_test_custom(check_group_and_activation, login_url='teacher/login')
def get_chats(request):
    chats = Chat.objects.filter(members__in=[request.user.id])
    return render(request, 'teacher/chat/chats.html', {'user_profile': request.user, 'chats': chats})


@user_passes_test_custom(check_group_and_activation, login_url='teacher/login')
def get_chat_with_user(request, chat_id):
    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('teacher:messages', kwargs={'chat_id': chat_id}))
    else:
        chats = Chat.objects.filter(members__in=[request.user.id])
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'teacher/chat/messages.html',{
                'user_profile': request.user,
                'chat': chat,
                'chats': chats,
                'form': MessageForm()}
        )


@user_passes_test_custom(check_group_and_activation, login_url='teacher/login')
def start_chat_with_user(request, user_id):
    chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
    if chats.count() == 0:
        chat = Chat.objects.create()
        chat.members.add(request.user)
        chat.members.add(user_id)
    else:
        chat = chats.first()
    return redirect(reverse('teacher:messages', kwargs={'chat_id': chat.id}))
