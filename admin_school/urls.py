from django.urls import path
# from .views import Logout_View
# from .views import Login_View
from .views import main_page_view
from .views import group_list_view
from .views import student_card
from .views import timetable
from .views import revise_timetable
from .views import teachers_view
from .views import news_view
from .views import rubrick
from .views import NewsAdd
from .views import change_new
from .views import new_view
from .views import delete_new
from .views import AddRubrick
from .views import change_rubrick
from .views import delete_rubrick
from .views import costs
from .views import costs_admin
from .views import login_user
from .views import logout_request


app_name = 'admin_school'


urlpatterns = [
    path('del_rubrick/<int:id>', delete_rubrick, name='delete_rubrick'),
    path('change_rubrick/<int:id>', change_rubrick, name='change_rubrick'),
    path('add_rubrick/', AddRubrick.as_view(), name='add_rubrick'),
    path('costs/', costs, name='costs'),
    path('costs_admin/', costs_admin, name='costs_admin'),
    path('del_new/<int:pk>', delete_new, name='del_new'),
    path('new/<int:pk>', new_view, name='new_view'),
    path('change_new/<int:pk>', change_new, name='change_new'),
    path('add_news', NewsAdd.as_view(), name='add_news'),
    path('<int:pk>/', rubrick, name='rubrick'),
    path('news/', news_view, name="news"),
    path('teacher_tab', teachers_view, name='teacher_tab'),
    path('timetable/', timetable, name='timetable'),
    path('revise_timetable/<int:pk>/', revise_timetable, name='revise_timetable'),
    path('card_student/<id>/', student_card, name='student_card'),
    path('group_list/', group_list_view, name='group_list_view' ),
    # path("logout_admin/", logout_request,name='logout_admin'),
    # path("autorization_page_admin/", login_user,name="autorization_page_admin"),
    path("logout/", logout_request, name='logout'),
    path("login/", login_user, name="login"),
    path('', main_page_view, name='main_page_view'),

]