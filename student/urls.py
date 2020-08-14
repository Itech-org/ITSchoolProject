from django.urls import path
from .views import *


app_name = 'student'

urlpatterns = [
    path("logout/",Logout_View.as_view(),name='logout'),
    path("login/",Login_View.as_view(),name="login"),
    path('change_data/', Change_user_info, name='change_data'),
    path('', main_page_view, name='main_page_view'),
    path('account/', account, name="account"),
    path('calendar/', calendar, name='calendar'),
    path('process/', process, name='process'),
    path('my_group/<int:group_id>/', group_view, name="group_view"),
    path('group_profile/<int:user_id>/', group_profile, name='group_profile'),
    path('teachers/', teacher_view, name='teacher'),
    path('teacher_profile/<int:teacher_id>/', teacher_profile, name='teacher_profile'),
    path('my_courses/', my_courses, name="my_courses"),
    path('my_courses/<int:course_id>/', exact_course, name="exact_course"),
    path('homework/', homework_view, name="homework"),
    path('exact_hw/<int:homework_id>/', exact_homework, name='exact_hw'),
    path('materials/', materials_view, name="materials_view"),
    path('material_themes/', material_themes, name="material_themes"),
    path('material_detail/<int:class_id>/', material_detail, name="material_detail"),
    path('study_liter/', liter_view, name='study_literature'),
    path('video_materials/', video_materials, name="video_materials"),
    path('video_themes/', video_themes, name='video_themes'),
    path('video_detail/<int:class_id>/', video_detail, name='video_detail'),
    path('shedule/', shedule_view, name="shedule"),
    path('class/<int:class_id>/detail/', class_view, name="class_view"),
    path('contact_admin/', contact_admin, name="contact_admin"),
    path('itnews/', itnews, name="itnews"),
    path('services/', services, name="services"),
    path('chats/', get_chats, name='chats'),
    path('chat/create/<int:user_id>/', start_chat_with_user, name='create_dialog'),
    path('chat/<int:chat_id>', get_chat_with_user, name='messages'),
    path('api/v1/classes-list/', api_classes_list)
]
