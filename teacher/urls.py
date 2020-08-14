from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'teacher'

urlpatterns = [
    path('', index, name='index'),
    path("login/",Login_View.as_view(),name="login"),
    path("logout/",Logout_View.as_view(),name='logout'),
    path('profile/', profile, name="profile"),
    path('account/', account, name="account"),
    path('calendar/', calendar, name='calendar'),
    # path('calendar/<int:class_id>/', class_detail, name='class_detail'),
    path('study_procces/', study_procces, name='study_procces'),
    path('student_<int:student_id>/', student_detail, name='student_detail'),
    path('group/', group_detail, name="group_detail"),
    path('materials/', materials, name='materials'),
    path('literature/', text_mat, name='text_mat'),
    path('literature/<slug:slug_l>/', text_detail, name='text_detail'),
    path('video/', video_mat, name='video_mat'),
    path('video/<slug:slug_v>/', video_detail, name='video_detail'),
    path('homework/', homework, name="homework"),
    path('homework_detail/<int:hw_id>/', homework_detail, name="homework_detail"),
    path('materials_on_theme/', materials_on_theme, name="materials_on_theme"),
    path('material_detail/', material_detail, name="material_detail"),
    path('video_courses/', video_courses, name="video_courses"),
    path('video_courses/<int:cs_id>/', vd_crs_detail, name="vd_crs_detail"),
    path('chat/', chat, name="chat"),
    path('teachers/', teachers, name="teachers"),
    path('news/', news, name="news"),
    path('password/', MyPasswordChange.as_view(), name='password'),
    path('password_reset/', MyPasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
