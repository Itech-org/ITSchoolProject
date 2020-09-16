from .models import Notification, PersonalNotification

def get_unread_chats_count(request):
    if request.user.is_authenticated:
        return {'unreaded_dialogs_counter': request.user.chat_set.unreaded(user=request.user).count()}
    else:
        return {'unreaded_dialogs_counter': 0}


def get_notification_student(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Student'):
                notifications = []
                group_notifications = Notification.objects.filter(recipient__students=request.user)
                personal_notifications = PersonalNotification.objects.filter(recipient=request.user)
                if group_notifications:
                    for elem in group_notifications:
                        notifications.append(elem)
                if personal_notifications:
                    for elem in personal_notifications:
                        notifications.append(elem)
                notifications = sorted(notifications, key=lambda object: object.date, reverse=True)
                return {'notifications': notifications}
        else:
            return {}
    else:
        return {}