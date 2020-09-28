from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
from .forms import LoginForm
from .utilities import *
from manager_school.models import *


def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    return redirect("director_school:login")
                else:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    return redirect('director_school:main_page')
            else:
                return redirect("director_school:login")
        else:
            form = LoginForm()
            return render(request, 'director/other/login.html', {'form': form})
    else:
        return redirect('director_school:main_page')


@login_required
def logout_request(request):
    logout(request)
    return redirect("entry_page")


@user_passes_test_custom(check_group_and_activation, login_url='/director-school/login')
def main_page_view(request):
    return render(request, template_name='director/base_director.html')


# Расписание
@user_passes_test_custom(check_group_and_activation, login_url='/director-school/login')
def timetable(request):
    classes = ClassModel.objects.all()
    context = {"classes": classes}
    return render(request, "director/classes/timetable.html", context)

# Список групп
@user_passes_test_custom(check_group_and_activation, login_url='/director-school/login')
def group_list(request):
    groups = GroupModel.objects.all()
    # for group in groups:
    #     for student in group.students.all():
    #         performance = AdvUser.objects.annotate(perf=student.get_academic_performance(group_id=group.id))
    context = {"groups":groups}
    return render(request, "director/classes/group_list.html", context)


# Менеджер
@user_passes_test_custom(check_group_and_activation, login_url='/director-school/login')
def manager_list(request):
    managers = AdvUser.objects.filter(groups__name="Manager")
    colspan = int(managers.count())+1
    request_dict = get_requests(managers)
    conversations = get_conversations(managers)
    contracts = get_contracts(managers)
    context = {'managers':managers, 'requests':request_dict, 'conversations':conversations, 'colspan':colspan, 'contracts':contracts}
    return render(request, "director/management/managers.html", context)


# Оплата
@user_passes_test_custom(check_group_and_activation, login_url='/director-school/login')
def payments(request):
    contracts = Contract.objects.all()
    user_payments = get_user_payments(contracts)
    context = {'contracts':contracts, 'payments':user_payments}
    return render(request, "director/management/payment.html", context)


# Расходы
@user_passes_test_custom(check_group_and_activation, login_url='/director-school/login')
def expences(request):
    expences = Expences.objects.all().order_by('group')
    spent = 0
    for exp in expences:
        spent += exp.price
    proceeds = 0
    payment_stages = PaymentStage.objects.filter(is_confirmed=True)
    for stage in payment_stages:
        proceeds += stage.price
    profit = proceeds - spent
    context = {'expences':expences, 'spent':spent, 'proceeds':proceeds, 'profit':profit}
    return render(request, "director/management/expences.html", context)