from django.urls import path

from .views import *

app_name = 'director_school'

urlpatterns = [
    path("logout/", logout_request, name='logout'),
    path("login/", login_user, name="login"),
    path("", main_page_view, name='main_page'),
    path("timetable/", timetable, name="timetable"),
    path("groups/", group_list, name="group_list"),
    path("managers/", manager_list, name="manager_list"),
    path("payments/", payments, name="payments"),
    path("expences/", expences, name="expences"),
    ]