import datetime
import urllib

from django import template
from django.template.defaulttags import register
from ..models import Attendance, CourseUser, ClassModel

# register = template.Library()


@register.simple_tag(name="get_performance")
def performance(obj, group_id=''):
    return obj.get_academic_performance(group_id)


@register.simple_tag(name="get_attendance")
def get_attendance(obj, group_id=''):
    return obj.get_attendance(group_id)


@register.simple_tag
def get_companion(advuser, chat):
    for u in chat.members.all():
        if u != advuser:
            return u
    return None


@register.simple_tag
def get_unread_message_count(advuser, chat):
    """Выводит кодичество непрочитанных сообщений в чате"""
    count = chat.message_set.exclude(author=advuser).filter(is_readed=False).count()
    return count


@register.simple_tag
def string_split(string):
    return urllib.parse.unquote(string.split(r'/')[-1])


@register.simple_tag
def get_student_attendance(student, class_):
    """Возвращает посещение ученика за переданное занятие"""
    try:
        attendance = Attendance.objects.filter(classes=class_, students=student)[0]
    except IndexError:
        attendance = []
    return attendance


@register.simple_tag
def get_teacher_courses(teacher, student=None):
    """Возвращает посещение ученика за переданное занятие"""
    if student:
        courses = CourseUser.objects.filter(groups__in=teacher.groups_teacher.filter(students__id=student.id))
    else:
        courses = CourseUser.objects.filter(groups__in=teacher.groups_teacher.all())
    return set(courses)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def get_room_at_current_day(room, date, interval):
    """Возвращаем занятие текущего дня заданной аудитории и времени"""
    class_data = ClassModel.objects.filter(
        classroom=room,
        date=date,
        start_time__gte=interval.time_from,
        end_time__lte=interval.time_to
    )
    return class_data


@register.simple_tag
def check_current_date(date):
    return date == datetime.date.today()