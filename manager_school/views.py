from django.contrib.auth import authenticate, login

from django.db.models import Count
from django.http import HttpResponseRedirect, QueryDict

from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filters import StudyRequestFilter, GroupFilter
from .forms import *
from django.shortcuts import render

from .serializers import ClassModelSerializer

from .utilities import *


def login_user(request):
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


def logout_request(request):
    logout(request)
    return redirect("manager_school:login")


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def main_page_view(request):
    return render(request, template_name='manager/base_manager.html')


# ---------------------groups-----------------------------


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_groups(request):
    query_dict = QueryDict('', mutable=True)
    query_dict.update(request.GET)
    if 'manager' not in query_dict:
        query_dict['manager'] = f"{request.user.id}"

    groups = GroupFilter(data=query_dict, queryset=GroupModel.objects.all())
    managers = AdvUser.objects.filter(groups__name='Manager')
    teachers = AdvUser.objects.filter(groups__name='Teacher')
    courses = CourseUser.objects.all()
    return render(request, "manager/group/group-list.html", {
        "groups": groups,
        "managers": managers,
        "teachers": teachers,
        "courses": courses
    })


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def add_group(request):
    if request.method == "POST":
        group_form = GroupModelForm(request.POST)
        if group_form.is_valid():
            group = group_form.save()
            return redirect('manager_school:create_group_classes', slug=group.slug)
    else:
        group_form = GroupModelForm(initial={"manager": request.user})
    return render(request, "manager/group/create_group.html", {
        "group_form": group_form,
    })


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def create_group_classes(request, slug):
    group = get_object_or_404(GroupModel, slug=slug)
    course = group.course
    count_days = course.finish_date - course.start_date
    class_rooms = Classroom.objects.all()
    if request.method == "POST":
        if 'classes_days' in request.POST and 'class_room' in request.POST:
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            days_list = [int(day) for day in request.POST.getlist('classes_days')]
            position = 1
            class_room = get_object_or_404(Classroom, title=request.POST["class_room"])
            for day in range(count_days.days + 1):
                dt = course.start_date + datetime.timedelta(day)
                if dt.weekday() in days_list:
                    ClassModel.objects.create(
                        position=position,
                        theme=f'Тема-{position}',
                        groups=group,
                        classroom=class_room,
                        date=dt,
                        start_time=start_time,
                        end_time=end_time
                    )
                    position += 1
            return redirect("manager_school:get_group_detail", slug=slug)
    else:
        pass
    return render(request, "manager/class/create_group_classes.html", {"course": course, "group": group, "class_rooms": class_rooms})



@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_group_detail(request, slug):
    group = get_object_or_404(GroupModel, slug=slug)
    try:
        next_lesson = ClassModel.objects.filter(groups__slug=slug, date__gt=datetime.datetime.now())[0]
    except IndexError:
        next_lesson = []
    try:
        prev_lesson = ClassModel.objects.filter(
            groups__slug=slug, date__lt=datetime.datetime.now()
        ).order_by('-date')[0]
    except IndexError:
        prev_lesson = []
    return render(request, "manager/group/group_detail.html", {
        "group": group, "next_lesson": next_lesson, "prev_lesson": prev_lesson})


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
    attendances = Attendance.objects.filter(classes__id=class_id)
    return render(request, "manager/class/class_detail.html", {
        "class": class_data,
        "attendances": attendances,
    })


# ---------------------leads-----------------------------

@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_leads(request):
    leads = StudyRequestFilter(request.POST, queryset=StudyRequest.objects.all())
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
        lead_form = StudyRequestForm(initial={"specialist": request.user, 'enter_date': datetime.datetime.now()})
    return render(request, "manager/lead/create_lead.html", {
        "lead_form": lead_form,
    })


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def lead_history(request, lead_id):
    lead = get_object_or_404(StudyRequest, id=lead_id)
    conversations = lead.requestconversation_set.all()
    conversation_form = RequestConversationForm(initial={'request': lead})
    if request.method == "POST":
        lead_form = StudyRequestForm(request.POST, instance=lead)
        if lead_form.is_valid():
            lead_form.save()
            return redirect('manager_school:lead_history', lead_id=lead_id)
    else:
        lead_form = StudyRequestForm(instance=lead)
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
            form.save()
            return redirect('manager_school:create_contract_page', lead_id=lead_id)
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
    return render(request, 'manager/other/student_registrtion.html', {'form': form})


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def create_contract_page(request, lead_id):
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
        contract_form = ContractForm(initial={'date': datetime.datetime.now(), "lead": lead_id})
    return render(request, 'manager/contract/contract_create.html', {"contract_form": contract_form})


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def add_payment_stage(request, contract_id, payment_id):
    if request.method == "POST":
        payment_stage_form = PaymentStageForm(request.POST, request.FILES)
        if payment_stage_form.is_valid():
            payment_stage_form.save()
    else:
        payment = get_object_or_404(UserPayment, id=payment_id)
        payment_stage_form = PaymentStageForm(initial={'payment': payment})
    payment_stages = PaymentStage.objects.filter(payment__id=payment_id)
    return render(request, 'manager/contract/payment_stage_create.html', {"payment_stage_form": payment_stage_form,
                                                                     "payment_stages": payment_stages,
                                                                     "contract_id": contract_id})


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
def start_chat_with_user(request, user_id):
    chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
    if chats.count() == 0:
        chat = Chat.objects.create()
        chat.members.add(request.user)
        chat.members.add(user_id)
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


# ---------------------profile-----------------------------


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def get_manager_profile(request):
    data = get_manager_data_per_period(request.user)

    context = {
        'successful_leads_percent': get_manager_successful_percent(request.user, model='StudyRequest'),
        'successful_contracts_percent': get_manager_successful_percent(request.user, model='Contract'),
        'data': data,
    }
    return render(request, 'manager/profile/profile.html', context)


@user_passes_test_custom(check_group_and_activation, login_url='/manager-school/login')
def change_user_info(request):
    if request.method == "POST":
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        print(request.FILES)
        img_user = request.FILES.get('img_user', '')
        print(img_user)
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