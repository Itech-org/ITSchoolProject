from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic.edit import CreateView
from admin_school.forms import ClassModelForm, NewsForm, RubrickForm
from manager_school.utilities import user_passes_test_custom
from django.shortcuts import get_object_or_404, get_list_or_404
from manager_school.models import GroupModel, AdvUser, ClassModel, News, RubruckNews
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound


class Login_View(LoginView):
    template_name = 'admin/main_page/autorization_page_admin.html'


class Logout_View(LogoutView):
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


@user_passes_test_custom(check_group_and_activation, login_url='/admin_school/autorization_page_admin')
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
    timetab = ClassModel.objects.order_by('date')
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
        return render(request, "admin/main_page/timetable/revise_timetable.html",
                      {"rev_timetable": rev_timetable, 'form': form})

    except ClassModel.DoesNotExist:
        return HttpResponseNotFound("<h2>not found</h2>")


def news_view(request):
    news = News.objects.all()
    rubricks = RubruckNews.objects.all()
    context = {"news": news, 'rubricks': rubricks}
    return render(request, 'admin/main_page/news/news.html', context)


def rubrick(request, pk):
    news_rubrick = RubruckNews.objects.get(pk=pk)
    current_news = news_rubrick.news_set.all()
    paginator = Paginator(current_news, 2)
    if "page" in request.GET:
        page_num = request.GET["page"]
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'news_rubrick': news_rubrick, "current_news": page.object_list, 'page': page, }
    return render(request, 'admin/main_page/news/rubrick.html', context)


class NewsAdd(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'admin/main_page/news/news_add_form.html'
    success_url = 'news/'


def new_view(request, pk):
    new = get_object_or_404(News, pk=pk)
    return render(request, 'admin/main_page/news/new.html', {'new': new})


def change_new(request, pk):
    change_news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=change_news)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.save()
            return HttpResponseRedirect('../news')
    else:
        form = NewsForm(instance=change_news)
    context = {'change_news': change_news, 'form': form}
    return render(request, 'admin/main_page/news/change_new.html', context)


def delete_new(request, pk):
    new = News.objects.get(pk=pk).delete()
    return HttpResponseRedirect('../news')


class AddRubrick(CreateView):
    model = RubruckNews
    form_class = RubrickForm
    template_name = 'admin/main_page/news/add_rubrick.html'
    success_url = '/admin_school/'


def change_rubrick(request, id):
    change_rubricks = get_object_or_404(RubruckNews, id=id)
    if request.method == 'POST':
        form = RubrickForm(request.POST, instance=change_rubricks)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.save()
            return HttpResponseRedirect('../news')
    else:
        form = RubrickForm(instance=change_rubricks)
    context = {'change_rubricks': change_rubricks, 'form': form}
    return render(request, 'admin/main_page/news/change_rubrick.html', context)


def delete_rubrick(request, id):
    new = RubruckNews.objects.get(id=id).delete()
    return HttpResponseRedirect('../news')

