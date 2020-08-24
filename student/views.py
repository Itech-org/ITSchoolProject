from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from manager_school.utilities import user_passes_test_custom
from django.shortcuts import get_object_or_404, get_list_or_404
from manager_school.models import *
from manager_school.forms import MessageForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ClassModelSerializer
from .utilities import *
from .forms import *
import datetime


# Create your views here.
from manager_school.forms import MessageForm
from manager_school.models import Chat


def check_group_and_activation(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Student").exists():
            return True
        else:
            logout(request)
            return False
    else:
        return False


def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    return redirect("student:login")
                else:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    return redirect('student:main_page_view')
            else:
                return redirect("student:login")
        else:
            form = LoginForm()
            return render(request, 'student/authorization_page.html', {'form': form})
    else:
        return redirect('student:main_page_view')


def logout_request(request):
    logout(request)
    return redirect("student:login")


# class Login_View(LoginView):
#     template_name = 'student/login.html'


class Logout_View(LoginRequiredMixin, LogoutView):
    template_name = "student/logout.html"


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def Change_user_info(request):
    if request.method == "POST":
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        img_user = request.FILES.get('img_user', '')
        user = request.user
        if phone:
            user.phone = phone
        if email:
            user.email = email
        if img_user:
            user.img_user = img_user
        user.save()
        return redirect('student:account')
    return render(request, 'student/change_personal_data.html')




@user_passes_test_custom(check_group_and_activation, login_url='/login')
def main_page_view(request):
    my_id = request.user.id
    my_groups = GroupModel.objects.filter(students__id=my_id)
    course = [x.course for x in my_groups]
    teachers = [x.teacher for x in my_groups]
    context = {'teachers': teachers, 'groups': my_groups, 'course': course}
    return render(request, 'student/main_page_student.html', context)


@login_required
def account(request):
    student = get_object_or_404(AdvUser, id=request.user.id)
    attendance = Attendance.objects.filter(students__id=request.user.id)
    homework = HomeworkModel.objects.filter(user__id=request.user.id)
    payments = UserPayment.objects.filter(contract__account__id=request.user.id)
    unpaid = 0
    for payment in payments:
        if payment.is_paid == False:
            unpaid += 1
    context = {'student': student, 'attendance': attendance, 'homework': homework, 'unpaid':unpaid}
    return render(request, "student/students_personal_card.html", context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def my_courses(request):
    my_id = request.user.id
    group = get_object_or_404(GroupModel, students__id=my_id)
    courses = group.course.all()
    context = {'courses': courses}
    return render(request, "student/my_courses.html", context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def exact_course(request, course_id):
    course = get_object_or_404(CourseModel, id=course_id)
    context = {'course': course}
    return render(request, "student/exact_course.html", context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def homework_view(request):
    group = request.GET.get('group', '')
    groups = request.user.groupmodel_set.all()
    if group == '':
        current_group = groups[0]
        classes = ClassModel.objects.filter(groups__id=current_group.id).filter(date__lte=datetime.date.today())
    else:
        group_id = int(group)
        current_group = get_object_or_404(GroupModel, id=group_id)
        classes = current_group.classes.filter(date__lte=datetime.date.today())
    if classes.count() > 1:
        all_classes = [cls for cls in classes]
        last_class = all_classes[-1]
        next_class = current_group.classes.get(position=int(last_class.position + 1))
        all_classes.append(next_class)
    else:
        all_classes = classes
    context = {'groups': groups, 'group': current_group, 'classes': all_classes}
    return render(request, 'student/homework_on_topics.html', context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def exact_homework(request, homework_id):
    homework = HomeworkModel.objects.filter(id=homework_id)
    hw_id = [x.id for x in homework]
    cls = ClassModel.objects.filter(homework__id__in=hw_id)
    context = {'homework': homework, 'cls': cls}
    return render(request, "student/exact_homework.html", context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def shedule_view(request):
    my_id = request.user.id
    group = get_object_or_404(GroupModel, students__id=my_id)
    group_id = group.id
    shedule = get_object_or_404(SheduleModel, group__id=group_id)
    shedule_id = shedule.id
    cls = get_list_or_404(ClassModel, timetable__id=shedule_id)
    context = {'shedule': shedule, 'class': cls}
    return render(request, "student/shedule.html", context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def calendar(request):
    group = request.GET.get('group', '')
    groups = request.user.groupmodel_set.all()
    if group == '':
        current_group = 'Выбрать курс...'
        closest_class = ClassModel.objects.filter(groups__students__id=request.user.id).filter(date__gte=datetime.datetime.now())
    else:
        group_id = int(group)
        current_group = get_object_or_404(GroupModel, id=group_id)
        closest_class = current_group.classes.filter(date__gte=datetime.datetime.now())
    return render(request, 'student/educational_calendar.html',
                  {'groups': groups, 'group': current_group, 'classes': closest_class})


@api_view(['GET'])
def api_classes_list(request):
    group = request.GET.get('group', '')
    if group == '':
        classes = ClassModel.objects.filter(groups__students__id=request.user.id)
    else:
        try:
            group_id = int(group)
            classes = ClassModel.objects.filter(groups__id=group_id)
        except ValueError:
            classes = ClassModel.objects.filter(groups__students__id=request.user.id)
    data = ClassModelSerializer(classes, many=True)
    return Response(data.data)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def class_view(request, class_id):
    cls = ClassModel.objects.get(id=class_id)
    student_homework = [homework for homework in cls.homework.filter(user__id=request.user.id)]
    tries = len(student_homework)
    try:
        teacher_homework = cls.homeworkteacher.get()
        attempts_left = teacher_homework.attempts - tries
    except:
        attempts_left = None
    if tries > 1:
        last_homework = student_homework[-1]
    elif tries == 0:
        last_homework = None
    else:
        last_homework = student_homework[0]
    description = request.POST.get('description', '')
    file = request.FILES.get('file', '')
    context = {'class': cls, 'tries': tries, 'attempts_left': attempts_left, 'homework': student_homework, 'last_homework': last_homework}
    if request.POST:
        homework = HomeworkModel(title='Домашнее задание ' + str(request.user.first_name), class_field=cls, user=request.user)
        if description:
            homework.description = description
        if file:
            homework.file = file
        homework.save()
        return redirect('student:class_view', class_id=class_id)
    return render(request, "student/homework.html", context)


# ---- ВКЛАДКА УЧЕБНОГО ПРОЦЕССА ----


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def process(request):
    return render(request, 'student/studying_proccess.html')


# ---- ПРЕПОДАВАТЕЛИ ----


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def teacher_view(request):
    my_id = request.user.id
    my_groups = GroupModel.objects.filter(students__id=my_id)
    teachers = [x.teacher for x in my_groups]
    context = {'teachers': teachers, 'groups': my_groups}
    return render(request, 'student/teachers_new.html', context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(AdvUser, id=teacher_id)
    group = get_object_or_404(GroupModel, teacher_id=teacher_id, students__id=request.user.id)
    return render(request, 'student/teacher_card.html', {'teacher': teacher, 'group': group})


# ---- ВЫВОД МАТЕРИАЛОВ ----


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def materials_view(request):
    return render(request, 'student/studying_materials.html')


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def material_themes(request):
    group = request.GET.get('group', '')
    groups = request.user.groupmodel_set.all()
    if group == '':
        current_group = groups[0]
        classes = ClassModel.objects.filter(groups__id=current_group.id).filter(date__lte=datetime.date.today())
    else:
        group_id = int(group)
        current_group = get_object_or_404(GroupModel, id=group_id)
        classes = current_group.classes.filter(date__lte=datetime.date.today())
    if classes.count() > 1:
        all_classes = [cls for cls in classes]
        last_class = all_classes[-1]
        next_class = current_group.classes.get(position=int(last_class.position + 1))
        all_classes.append(next_class)
    else:
        all_classes = classes
    context = {'groups': groups, 'group': current_group, 'classes': all_classes}
    return render(request, 'student/materials_on_topics.html', context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def material_detail(request, class_id):
    cls = ClassModel.objects.get(id=class_id)
    materials = cls.materialtext_set.all()
    video_materials = cls.materialvideo_set.all()
    context = {'materials': materials, 'class': cls, 'v_materials': video_materials}
    return render(request, 'student/selected-lesson.html', context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def liter_view(request):
    materials = MaterialText.objects.all()
    context = {'materials': materials}
    return render(request, 'student/education-literature.html', context)


# ---- ВЫВОД ВИДЕОМАТЕРИАЛОВ ----


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def video_materials(request):
    video = MaterialVideo.objects.all()
    return render(request, 'student/video-material.html', {'video': video})


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def video_themes(request):
    group = request.GET.get('group', '')
    groups = request.user.groupmodel_set.all()
    if group == '':
        current_group = groups[0]
        classes = ClassModel.objects.filter(groups__id=current_group.id).filter(
            date__lte=(datetime.date.today() + datetime.timedelta(days=1)))
    else:
        group_id = int(group)
        current_group = get_object_or_404(GroupModel, id=group_id)
        classes = current_group.classes.filter(date__lte=(datetime.date.today() + datetime.timedelta(days=1)))
    if classes.count() > 1:
        all_classes = [cls for cls in classes]
        last_class = all_classes[-1]
        next_class = current_group.classes.get(position=int(last_class.position + 1))
        all_classes.append(next_class)
    else:
        all_classes = classes
    context = {'groups': groups, 'group': current_group, 'classes': all_classes}
    return render(request, 'student/video_on_topics.html', context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def video_detail(request, class_id):
    cls = ClassModel.objects.get(id=class_id)
    video_materials = MaterialVideo.objects.filter(class_field__id=class_id)
    context = {'class': cls, 'v_material': video_materials}
    return render(request, 'student/videolesson.html', context)


# ---- ВЫВОД ГРУППЫ ----


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def group_view(request):
    groups, current_group = group_filter(request)
    students = AdvUser.objects.filter(groupmodel__id=current_group.id)
    teachers = [x.teacher for x in groups]
    context = {'students': students, 'teachers': teachers, 'groups': groups, 'group': current_group}
    return render(request, 'student/group.html', context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def group_profile(request, user_id):
    student = get_object_or_404(AdvUser, id=user_id)
    attendance = Attendance.objects.filter(students__id=user_id)
    homework = HomeworkModel.objects.filter(user__id=user_id)
    context = {'student': student, 'attendance': attendance, 'homework': homework}
    return render(request, 'student/card_of_another_student.html', context)


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def contact_admin(request):
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
        return redirect(reverse('student:messages', kwargs={'chat_id': chat.id}))
    return render(request, 'student/contact_administrator.html')


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def itnews(request):
    rubrick = request.GET.get('rubrick', '')
    rubricks = RubruckNews.objects.all()
    if rubrick == '':
        news = News.objects.all()
        current_rubrick = None
    else:
        rubrick_id = int(rubrick)
        current_rubrick = RubruckNews.objects.get(id=rubrick_id)
        news = News.objects.filter(rubrick__id=rubrick_id)
    context = {'news':news, 'rubricks':rubricks, 'current_rubrick':current_rubrick}
    return render(request, 'student/itnews.html', context)


def news_detail(request, news_id):
    news = News.objects.get(id=news_id)
    created = f"{news.created.strftime('%d.%m.%Y')}"
    return render(request, 'student/container_news.html', {'news':news, 'created':created})


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def services(request):
    return render(request, 'student/services_page.html')


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def payment(request):
    groups, current_group = group_filter(request)
    user_payment = get_user_payment(request, current_group)
    if user_payment == None:
        return redirect(reverse('student:account'))
    else:
        payment_stages = get_payment_stages(request, current_group)
        if user_payment.by_stages == True:
            percentage, paid_amount, stages_amount = get_paid_percent(payment_stages)
            context = {
                'group': current_group, 'groups': groups,
                'payment_stages': payment_stages, 'payment': user_payment,
                'percentage': percentage, 'paid_amount': paid_amount,
                'stages_amount': stages_amount
            }
        else:
            context = {
                'group': current_group, 'groups': groups,
                'payment_stages': payment_stages, 'payment': user_payment
            }
        picture = request.FILES.get('picture', '')
        if picture:
            save_picture(request, payment_stages, picture)
            payment_stages = get_payment_stages(request, current_group)
            context.update({'payment_stages':payment_stages})
            if user_payment.by_stages == True:
                alert = get_alert(request, payment_stages)
                context.update({'alert':alert})
        return render(request, 'student/payment_stages.html', context)
# ---- ЧАТ ----


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def get_chats(request):
    chats = Chat.objects.filter(members__in=[request.user.id])
    return render(request, 'student/chat/chats.html', {'user_profile': request.user, 'chats': chats})


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def get_chat_with_user(request, chat_id):
    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('student:messages', kwargs={'chat_id': chat_id}))
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

        return render(request,'student/chat/messages.html',{'user_profile': request.user,'chat': chat,'chats': chats,'form': MessageForm()})


@user_passes_test_custom(check_group_and_activation, login_url='/login')
def start_chat_with_user(request, user_id):
    chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
    if chats.count() == 0:
        chat = Chat.objects.create()
        chat.members.add(request.user)
        chat.members.add(user_id)
    else:
        chat = chats.first()
    return redirect(reverse('student:messages', kwargs={'chat_id': chat.id}))
