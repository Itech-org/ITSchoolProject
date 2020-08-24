from manager_school.models import Notification, ClassModel
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=ClassModel)
def receiver_function(sender, instance, **kwargs):
    a = ("Изменение в занятиях группы: {},"
         " занятия будут проходить в комнате {},"
         " дата занятия {}"
         " причина переноса: {}".format(instance.groups, instance.classroom.title, instance.date, instance.message))
    kek = Notification.objects.create(sender=instance, recipient=instance.groups,
                                      message=a, recieved_date=instance.date)
    kek.save()