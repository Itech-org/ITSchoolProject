from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from admin_school.forms import ClassModelForm
from manager_school.utilities import user_passes_test_custom
from django.shortcuts import get_object_or_404, get_list_or_404
from manager_school.models import GroupModel, AdvUser, ClassModel
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from .signals import receiver_function


class Login_View(LoginView):
    template_name = 'admin/main_page/autorization_page_admin.html'


class Logout_View(LoginRequiredMixin, LogoutView):
    template_name = "admin/logout_admin.html"


def check_group_and_activation(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Admin").exists():
            return True
        else:
            logout(request)
            return False
    else:
        return False


@user_passes_test_custom(check_group_and_activation, login_url='/admin-school/autorization_page_admin')
def main_page_view(request):
    return render(request, template_name='admin/main_page/main_page_admin.html')

# Список групп


def group_list_view(request):
    groups = get_list_or_404(GroupModel)
    context = {'groups': groups}
    return render(request, 'admin/main_page/group_list/number_group.html', context)

# Карточка студента


def student_card(request, id):
    user_id = id
    card = get_object_or_404(AdvUser, id=user_id)
    context = {'info': card}
    return render(request, 'admin/main_page/group_list/card_student.html', context)


def timetable(request):
    timetab = ClassModel.objects.all()
    context = {"timetab": timetab}
    return render(request, "admin/main_page/timetable/timetable.html", context)


def teachers_view(request):
    teachers = AdvUser.objects.filter(groups__name='Teacher')
    context = {"teachers": teachers}
    return render(request, 'admin/main_page/teacher/teacher_tab.html', context)


def revise_timetable(request, pk):
    try:
        rev_timetable = get_object_or_404(ClassModel, pk=pk)
        if request.method == 'POST':
            form = ClassModelForm(request.POST, instance=rev_timetable)
            if form.is_valid():
                form1 = form.save(commit=False)
                form1.save()
                return HttpResponseRedirect("../../timetable")
        else:
            form = ClassModelForm(instance=rev_timetable)
        return render(request, "admin/main_page/timetable/revise_timetable.html", {"rev_timetable": rev_timetable, 'form': form})

    except ClassModel.DoesNotExist:
        return HttpResponseNotFound("<h2>not found</h2>")