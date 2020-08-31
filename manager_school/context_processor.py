from .models import Notification

def get_unread_chats_count(request):
    if request.user.is_authenticated:
        return {'unreaded_dialogs_counter': request.user.chat_set.unreaded(user=request.user).count()}
    else:
        return {'unreaded_dialogs_counter': 0}


def get_notification_student(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Student'):
                notifications = Notification.objects.filter(recipient__students=request.user)
                print(notifications)
                if notifications:
                    notifications.order_by('-recieved_date')
                    return {'notifications':notifications}
        else:
            return {}
    else:
        return {}