from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from .filters import StudyRequestFilter
from .forms import *
from django.shortcuts import render

from .serializers import ClassModelSerializer, StudyRequestSerializer, CourseSerializer, CourseDetailSerializer
from .services import get_manager_successful_lead_percent, get_manager_data_per_period, get_planning_rooms, \
    create_group_classes, get_year_and_month, get_time_intervals


from .utilities import *


def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    return redirect("manager_school:login")
                else:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    return redirect('manager_school:main_page')
            else:
                return redirect("manager_school:login")
        else:
            form = LoginForm()
            return render(request, 'manager/other/login.html', {'form': form})
    else:
        return redirect('manager_school:main_page')


@login_required
def logout_request(request):
    logout(request)
    return redirect("entry_page")


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def main_page_view(request):
    return render(request, template_name='manager/base_manager.html')


# ---------------------groups-----------------------------


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_groups(request):
    course_id = request.GET.get('course')
    all_courses = CourseUser.objects.all()
    if course_id:
        courses = CourseUser.objects.filter(id=int(course_id))
        if courses.exists():
            selected_course = courses[0]
        else:
            selected_course = None
    else:
        courses = CourseUser.objects.all()
        selected_course = None
    return render(request, "manager/group/group-list.html", {
        "courses": courses,
        'selected_course': selected_course,
        'all_courses': all_courses,
    })


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def add_group(request):
    if request.method == "POST":
        group_form = GroupModelForm(request.POST)
        context = {'group_form': group_form}
        if group_form.is_valid():
            groups = GroupModel.objects.all()
            group_list = []
            for gp in groups:
                if gp.title == request.POST.get('title'):
                    group_list.append(gp.title)
            if group_list:
                alert = f'Группа с именем {request.POST.get("title")} уже существует'
                context.update({'alert':alert})
            else:
                group = group_form.save()
                return redirect('manager_school:create_group_classes', slug=group.slug)
    else:
        group_form = GroupModelForm(initial={"manager": request.user})
        context = {'group_form':group_form}
    return render(request, "manager/group/create_group.html", context)


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def create_group_classes_page(request, slug):
    group = get_object_or_404(GroupModel, slug=slug)
    course = group.course
    count_days = course.finish_date - course.start_date
    class_rooms = Classroom.objects.all()
    time_intervals = get_time_intervals(request, count_days, group)
    year, month = get_year_and_month(request)
    context = get_planning_rooms(year, month)
    context.update({
        "course": course,
        "group": group,
        "class_rooms": class_rooms,
        'current_month': month,
        'current_year': year,
        'time_intervals':time_intervals,
    })
    if request.method == "POST":
        alert = create_group_classes(request, count_days, group)
        if alert == None:
            return redirect("manager_school:get_group_detail", slug=slug)
        elif alert == False:
            return render(request, "manager/class/create_group_classes.html", context=context)
        else:
            context.update({'alert':alert})
            return render(request, "manager/class/create_group_classes.html", context=context)
    return render(request, "manager/class/create_group_classes.html", context=context)


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def update_class_date_and_time(request, class_id):
    class_data = get_object_or_404(ClassModel, id=class_id)
    class_rooms = Classroom.objects.all()
    if request.method == "POST":
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        class_room_title = request.POST.get('classroom')
        message = request.POST.get('message')
        classroom = get_object_or_404(Classroom, title=class_room_title)
        time_interval = RoomTimeInterval.objects.get(room=classroom, time_from__lte=start_time, time_to__gte=end_time)
        if time_interval.classtime.filter(date=date).exclude(id=class_id):
            free_intervals = []
            for room in class_rooms:
                for interval in room.time_intervals.all():
                    if not interval.classtime.filter(date=date):
                        free_intervals.append(interval)
            alert = f'Невозможно перенести занятие. Аудитория занята в этот временной промежуток.'
            return render(request, "manager/class/update_class_date_and_time.html",
                          context={'class': class_data, 'class_rooms': class_rooms, 'alert':alert,
                                   'free_intervals':free_intervals})
        else:
            class_data.classroom = classroom
            class_data.date = date
            class_data.start_time = start_time
            class_data.end_time = end_time
            class_data.time_interval = time_interval
            class_data.message = message
            class_data.save()

        return redirect('manager_school:planning_rooms_page')
    else:
        return render(request, "manager/class/update_class_date_and_time.html",
                      context={'class': class_data, 'class_rooms': class_rooms})


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_planning_rooms_page(request):
    year, month = get_year_and_month(request)
    context = get_planning_rooms(year, month)
    context.update({
        'current_month': month,
        'current_year': year,
    })
    return render(
        request, "manager/group/planning_rooms_page.html",
        context=context
    )


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_group_detail(request, slug):
    group = get_object_or_404(GroupModel, slug=slug)
    group_chat = Chat.objects.filter(group=group).first()
    return render(request, "manager/group/group_detail.html", {
        "group": group, 'group_chat': group_chat})


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def group_settings(request, slug):
    group = get_object_or_404(GroupModel, slug=slug)
    teachers = AdvUser.objects.filter(groups__name="Teacher")
    managers = AdvUser.objects.filter(groups__name="Manager")
    context = {'group':group, 'teachers':teachers, 'managers':managers}
    if request.method == "POST":
        if request.POST.get('delete') == 'on':
            group.delete()
            return redirect('manager_school:get_groups')
        else:
            title = request.POST.get('title', '')
            teacher_POST = request.POST.get('teacher', '').split(' ')
            teacher = AdvUser.objects.get(groups__name='Teacher', first_name=teacher_POST[0], last_name=teacher_POST[1])
            manager_POST = request.POST.get('manager', '').split(' ')
            manager = AdvUser.objects.get(groups__name='Manager', first_name=manager_POST[0], last_name=manager_POST[1])
            postponed = request.POST.get('postponed', '')
            if title != group.title:
                group.title = title
            if teacher != group.teacher:
                group.teacher = teacher
            if manager != group.manager:
                group.manager = manager
            if postponed:
                group.course_postponation(postponed)
            group.save()
            alert = 'Изменения сохранены'
            context.update({'alert':alert})
            return render(request, "manager/group/group_settings.html", context)
    return render(request, "manager/group/group_settings.html", context)


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_group_journal(request, slug):
    group = get_object_or_404(GroupModel, slug=slug)
    classes = group.classes.all().filter(date__lt=datetime.date.today() + datetime.timedelta(days=7))

    return render(request, "manager/group/group_journal.html", {
        "group": group, "classes": classes})

# ---------------------students-----------------------------


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_student_card(request, group_id, student_id):
    student = get_object_or_404(AdvUser, id=student_id)
    try:
        contract = Contract.objects.filter(account__id=student_id, group__id=group_id)[0]
    except IndexError:
        contract = []
    return render(request, "manager/other/student_card.html", {"student": student, "contract": contract})


# ---------------------teachers-----------------------------


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_teachers(request):
    teachers = AdvUser.objects.filter(groups__name='Teacher')
    return render(request, "manager/other/teachers_list.html", {"teachers": teachers})


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_teacher_card(request, teacher_id):
    teacher = get_object_or_404(AdvUser, id=teacher_id)
    return render(request, "manager/other/teacher_card.html", {"teacher": teacher})


# ---------------------classes-----------------------------


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_classes(request):
    group = request.GET.get('group', '')
    if group == '':
        selected_group = group
        classes = ClassModel.objects.all()
    else:
        try:
            selected_group = int(group)
            classes = ClassModel.objects.filter(groups__id=selected_group)
        except TypeError:
            selected_group = group
            classes = ClassModel.objects.all()

    groups = GroupModel.objects.all()
    date_now = datetime.datetime.now()
    return render(request, "manager/other/calendar.html", {
        "classes": classes,
        "groups": groups,
        "selected_group": selected_group,
        "date_now": date_now,
    })


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_class_detail(request, class_id):
    class_data = get_object_or_404(ClassModel, id=class_id)
    course = class_data.groups.course
    attendances = Attendance.objects.filter(classes__id=class_id)
    return render(request, "manager/class/class_detail.html", {
        "class": class_data,
        "course": course,
        "attendances": attendances,
    })


# ---------------------leads-----------------------------

@csrf_exempt
def api_leads_list(request):
    """
    List all code leads, or create a new lead.
    """
    if request.method == 'GET':
        snippets = StudyRequest.objects.all()
        serializer = StudyRequestSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StudyRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_leads(request):
    print(request.POST)
    leads = StudyRequestFilter(request.GET, queryset=StudyRequest.objects.all())
    return render(request, "manager/lead/leads_list.html", {
        "leads": leads,
    })


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def confirm_lead(request, lead_id):
    lead = get_object_or_404(StudyRequest, id=lead_id)
    lead.specialist = request.user
    lead.status = "In Progress"
    lead.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def add_lead(request):
    if request.method == "POST":
        lead_form = StudyRequestForm(request.POST)
        if lead_form.is_valid():
            lead = lead_form.save()
            return redirect('manager_school:lead_history', lead_id=lead.id)
    else:
        lead_form = StudyRequestForm(initial={
            "specialist": request.user,
            'enter_date': datetime.datetime.now().strftime("%d.%m.%Y")
        })
    return render(request, "manager/lead/create_lead.html", {
        "lead_form": lead_form,
    })


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def lead_history(request, lead_id):
    lead = get_object_or_404(StudyRequest, id=lead_id)
    conversations = lead.requestconversation_set.all()
    conversation_form = RequestConversationForm(initial={'request': lead,
                                                         'date': datetime.datetime.now().strftime("%Y-%m-%d")})
    if request.method == "POST":
        lead_form = StudyRequestForm(request.POST, instance=lead)
        if lead_form.is_valid():
            lead_form.save()
            return redirect('manager_school:lead_history', lead_id=lead_id)
    else:
        lead_form = StudyRequestForm(instance=lead, initial={
            'enter_date': lead.enter_date.strftime("%Y-%m-%d")
        })
    return render(request, "manager/lead/lead_history.html", {
        "lead": lead,
        "lead_form": lead_form,
        "conversation_form": conversation_form,
        "conversations": conversations,
    })


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def add_req_conversation(request, lead_id):
    if request.method == "POST":
        conversation_form = RequestConversationForm(request.POST)
        if conversation_form.is_valid():
            conversation_form.save()
    return redirect('manager_school:lead_history', lead_id=lead_id)


# ---------------------contracts-----------------------------


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_contracts(request):
    contracts = Contract.objects.all()
    return render(request, "manager/contract/contracts.html", {
        "contracts": contracts,
    })


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_choice(request, lead_id):
    return render(request, "manager/contract/create_contract_choice.html", {"lead_id": lead_id})


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def register_user(request, lead_id):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('manager_school:create_contract_page', lead_id=lead_id, student_id=student.id)
    else:
        lead = get_object_or_404(StudyRequest, id=lead_id)
        try:
            form = RegistrationForm(initial={
                'first_name': lead.first_name,
                'last_name': lead.last_name,
                'surname': lead.patronymic,
                'phone': lead.tel_number,
                'email': lead.email,
            })
        except Exception as e:
            print(e)
            form = []
    return render(request, 'manager/other/student_registration.html', {'form': form})


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def register_user_unique(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('manager_school:main_page')
    else:
        form = RegistrationForm
    return render(request, 'manager/other/student_registration.html', {'form': form})


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def create_contract_page(request, lead_id, student_id):
    if request.method == "POST":
        contract_form = ContractForm(request.POST)
        if contract_form.is_valid():
            contract = contract_form.save()
            payment = UserPayment.objects.create(
                contract=contract,
                by_stages=True if request.POST.get('by_stages', '') == 'on' else False,
            )
            group = contract.group
            student = contract.account
            group.students.add(student)
            return redirect('manager_school:add_payment_stage', contract_id=contract.id, payment_id=payment.id)
    else:
        student = get_object_or_404(AdvUser, id=student_id)
        contract_form = ContractForm(
            initial={
                'date': datetime.datetime.now(),
                "lead": lead_id,
                'account': student
            })
    return render(request, 'manager/contract/contract_create.html', {"contract_form": contract_form})


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def add_payment_stage(request, contract_id, payment_id):
    payment = get_object_or_404(UserPayment, id=payment_id)
    add_new_stage = True
    if not payment.by_stages:
        if payment.paymentstage_set.count() == 1:
            add_new_stage = False
    if request.method == "POST":
        payment_stage_form = PaymentStageForm(request.POST, request.FILES)
        if add_new_stage:
            if payment_stage_form.is_valid():
                payment_stage_form.save()
    else:
        payment_stage_form = PaymentStageForm(initial={'payment': payment})
    if not payment.by_stages:
        if payment.paymentstage_set.count() == 1:
            add_new_stage = False
    payment_stages = PaymentStage.objects.filter(payment__id=payment_id)
    return render(request, 'manager/contract/payment_stage_create.html', {
        "payment_stage_form": payment_stage_form,
        "payment_stages": payment_stages,
        "contract_id": contract_id,
        'add_new_stage': add_new_stage,
    })


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    if request.method == "POST":
        check = request.POST.get('is_subscribed', '')
        if check == 'on':
            contract.is_subscribed = True
        elif check == "off":
            contract.is_subscribed = False
        contract.save()
    return render(request, "manager/contract/contract_detail.html", {"contract": contract})


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def confirm_payment_stage(request, payment_stage_id):
    if request.method == "POST":
        payment_stage = get_object_or_404(PaymentStage, id=payment_stage_id)
        payment_stage.is_confirmed = True
        payment_stage.save()
    return redirect(request.META.get('HTTP_REFERER'))


# ---------------------chats-----------------------------


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_chats(request):
    chats = Chat.objects.filter(members__in=[request.user.id])
    return render(request, 'manager/chat/chats.html', {'user_profile': request.user, 'chats': chats})


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_chat_with_user(request, chat_id):
    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('manager_school:messages', kwargs={'chat_id': chat_id}))
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
            'manager/chat/messages.html',{
                'user_profile': request.user,
                'chat': chat,
                'chats': chats,
                'form': MessageForm()}
        )


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def start_group_chat(request, slug):
    title = request.POST.get('chat_title', '')
    group = get_object_or_404(GroupModel, slug=slug)

    chats = Chat.objects.filter(group=group)
    if chats.exists():
        pass
    else:
        chat = Chat.objects.create()
        chat.type = "C"
        chat.members.add(*[user for user in group.students.all()])
        chat.members.add(group.teacher)
        chat.group = group
        chat.set_chat_title(title)
    return redirect(reverse('manager_school:get_group_detail', kwargs={'slug': slug}))


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def start_chat_with_user(request, user_id):
    chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
    if chats.count() == 0:
        chat = Chat.objects.create()
        chat.members.add(request.user)
        chat.members.add(user_id)
        companion = get_object_or_404(AdvUser, id=user_id)
        chat.chat_title = f"{companion.first_name} {companion.last_name}"
    else:
        chat = chats.first()
    return redirect(reverse('manager_school:messages', kwargs={'chat_id': chat.id}))


# ---------------------api-----------------------------


@api_view(['GET'])
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


@api_view(['GET'])
def api_online_course_list(request):
    courses = CourseUser.objects.filter(is_online=True)
    data = CourseSerializer(courses, many=True)
    return Response(data.data)


@api_view(['GET'])
def api_offline_course_list(request):
    courses = CourseUser.objects.filter(is_online=False)
    data = CourseSerializer(courses, many=True)
    return Response(data.data)


@api_view(['GET'])
def api_course_detail(request, course_id):
    course = get_object_or_404(CourseUser, id=course_id)
    data = CourseDetailSerializer(course)
    return Response(data.data)


# ---------------------profile-----------------------------


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_manager_profile(request):
    period_from = request.GET.get('period_from')
    period_to = request.GET.get('period_to')
    manager_data_per_period = get_manager_data_per_period(request.user, period_from=period_from, period_to=period_to)

    context = {
        'successful_leads_percent': get_manager_successful_lead_percent(request.user),
        'manager_data_per_period': manager_data_per_period,
    }
    return render(request, 'manager/profile/profile.html', context)


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def change_user_info(request):
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
        return redirect('manager_school:get_manager_profile')
    return render(request, 'manager/profile/change_personal_data.html')


# ---------------------news-----------------------------


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_news_list(request):
    return render(request, 'manager/other/news_list.html', {
        'news': News.objects.all()
    })


@csrf_exempt
def news_list(request):
    if request.method == "GET":
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return JsonResponse(serializer.data, safe=False)
