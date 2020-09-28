from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'teacher'

urlpatterns = [
    path('', index, name='index'),
    path("login/", login_user, name="login"),
    path("logout/", logout_request,name='logout'),
    path('profile_edit/', profile_edit, name="profile_edit"),
    path('profile/', profile, name="profile"),
    path('calendar/', calendar, name='calendar'),
    path('study_proccess/', study_procces, name='study_procces'),
    path('student_<int:student_id>/', student_detail, name='student_detail'),
    path('class/<int:class_id>/detail/', class_detail, name='class_detail'),
    path('group/', group_detail, name="group_detail"),
    path('materials/', materials, name='materials'),
    path('literature/', text_mat, name='text_mat'),
    path('literature/<int:l_id>/', text_detail, name='text_detail'),
    path('video/', video_mat, name='video_mat'),
    path('video/<slug:slug_v>/', video_detail, name='video_detail'),
    path('homework/', homework, name="homework"),
    path('homework_detail/<int:hw_id>/', homework_detail, name="homework_detail"),
    path('materials_on_theme/', materials_on_theme, name="materials_on_theme"),
    path('materials_on_theme/<int:class_id>/', material_detail, name="material_detail"),
    path('video_courses/', video_courses, name="video_courses"),
    path('video_courses/<int:cs_id>/', vd_crs_detail, name="vd_crs_detail"),
    path('teachers/', teachers, name="teachers"),
    path('teachers/<int:t_id>/', teacher_card, name='teacher_card'),
    path('news/', news, name="news"),
    path('news/<int:post_id>/', post_detail, name='post_detail'),
    path('message-for-admin/', message_for_admin, name='message_for_admin'),
    path('password/', MyPasswordChange.as_view(), name='password'),
    path('password_reset/', MyPasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/v1/classes-list/', api_classes_list),
    path('chats/', get_chats, name='chats'),
    path('chat/create/<int:user_id>/', start_chat_with_user, name='create_dialog'),
    path('chat/<int:chat_id>', get_chat_with_user, name='messages'),
]
