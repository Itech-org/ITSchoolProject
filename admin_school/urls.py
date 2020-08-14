from django.urls import path
from .views import Logout_View
from .views import Login_View
from .views import main_page_view
from .views import group_list_view
from .views import student_card
from .views import timetable
from .views import revise_timetable
from .views import teachers_view

app_name = 'admin_school'


urlpatterns = [
    path('teacher_tab', teachers_view, name='teacher_tab'),
    path('timetable/', timetable, name='timetable'),
    path('revise_timetable/<int:pk>/', revise_timetable, name='revise_timetable'),
    path('card_student/<id>/', student_card, name='student_card'),
    path('group_list/', group_list_view, name='group_list_view' ),
    path("logout_admin/",Logout_View.as_view(),name='logout_admin'),
    path("autorization_page_admin/",Login_View.as_view(),name="autorization_page_admin"),
    path('', main_page_view, name='main_page_admin'),

]