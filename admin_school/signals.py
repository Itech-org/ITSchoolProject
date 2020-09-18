from manager_school.models import Notification, ClassModel
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=ClassModel)
def receiver_function(sender, instance, **kwargs):
    if instance.message:
        date = datetime.strptime(instance.date, '%Y-%m-%d')
        text = f'''Изменения в занятиях группы {instance.groups.title}.
                Занятия будут проходить в аудитории №{instance.classroom.title},
                дата и время занятия: {date.strftime('%d-%m-%Y')} {instance.start_time}-{instance.end_time}.
                Причина переноса: {instance.message}.'''
        notification = Notification.objects.create(sender=instance, recipient=instance.groups,
                                          message=text, date=instance.date)
        notification.save()