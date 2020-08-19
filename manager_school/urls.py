from django.urls import path

from .views import *

app_name = 'manager_school'

urlpatterns = [
    path("logout/", logout_request, name='logout'),
    path("login/", login_user, name="login"),
    path('registration_user/<int:lead_id>/', register_user, name='registration_page'),
    path('profile/', get_manager_profile, name='get_manager_profile'),
    path('profile/change-user-info/', change_user_info, name='change_user_info'),
    path('', main_page_view, name='main_page'),
    path('groups/', get_groups, name='get_groups'),
    path('group/create/', add_group, name='add_group'),
    path('group/<str:slug>/add-classes', create_group_classes, name='create_group_classes'),
    path('group/<str:slug>/detail/', get_group_detail, name='get_group_detail'),
    path('group/<str:slug>/journal/', get_group_journal, name='get_group_journal'),
    path('group/<int:group_id>/student/<int:student_id>/card/', get_student_card, name='get_student_card'),
    path('classes/', get_classes, name='get_classes'),
    path('class/<int:class_id>/detail/', get_class_detail, name='get_class_detail'),
    path('teachers/', get_teachers, name='get_teachers'),
    path('teacher/<int:teacher_id>', get_teacher_card, name='get_teacher_card'),
    path('leads/', get_leads, name='get_leads'),
    path('lead-create/', add_lead, name='add_lead'),
    path('lead/<int:lead_id>/history/', lead_history, name='lead_history'),
    path('lead/<int:lead_id>/add/conversation/', add_req_conversation, name='add_req_conversation'),
    path('contracts/', get_contracts, name='get_contracts'),
    path('contracts/create/choice/<int:lead_id>/', get_choice, name='get_choice'),
    path('contracts/create/<int:lead_id>/', create_contract_page, name='create_contract_page'),
    path('contract/<int:contract_id>/payment/<int:payment_id>/add-stage/', add_payment_stage, name='add_payment_stage'),
    path('contract/<int:contract_id>/', get_contract_detail, name='get_contract_detail'),
    path('payment-stage/<int:payment_stage_id>/', confirm_payment_stage, name='confirm_payment_stage'),
    path('chats/', get_chats, name='chats'),
    path('chat/create/<int:user_id>/', start_chat_with_user, name='create_dialog'),
    path('chat/<int:chat_id>', get_chat_with_user, name='messages'),
    path('news/', get_news_list, name='get_news_list'),
    path('api/v1/classes-list/', api_classes_list)
]
