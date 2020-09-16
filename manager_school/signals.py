from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import Message, PersonalNotification, RequestConversation, StudyRequest, ContactAdmin


@receiver(post_save, sender=Message)
def post_save_comment(sender, instance, **kwargs):
    # указываем чату, в котором находится данное сообщение, что это последнее сообщение
    instance.chat.last_message = instance
    # и обновляем данный внешний ключ чата
    instance.chat.save(update_fields=['last_message'])


@receiver(post_save, sender=RequestConversation)
def signal_handler(sender, instance, **kwargs):
    request = get_object_or_404(StudyRequest, id=instance.request.id)
    status = instance.status
    if status == "Сall back":
        status = 'In Progress'
    request.status = status
    request.save()


@receiver(post_save, sender=ContactAdmin)
def request_complited(sender, instance, **kwargs):
    if instance.status == 'Completed':
        text = f"Ваша заявка от {instance.date.strftime('%d.%m.%Y')} была закрыта администратором {instance.admin}. Ответ администратора: {instance.response}"
        notification = PersonalNotification(recipient=instance.author, message=text)
        notification.save()
    if instance.status == 'In progress':
        text = f"Ваша заявка от {instance.date.strftime('%d.%m.%Y')} была принята в работу администратором {instance.admin}."
        notification = PersonalNotification(recipient=instance.author, message=text)
        notification.save()


# @receiver(pre_save, sender=AdvUser)
# def signal_handler(sender, instance, **kwargs):
#     instance.set_password(instance.password)