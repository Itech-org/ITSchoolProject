import datetime

from django.shortcuts import get_object_or_404

from .models import Contract, AdvUser, Classroom, ClassModel


def get_manager_leads(user):
    return user.studyrequest_set.all()


def get_manager_successful_leads(user):
    return user.studyrequest_set.filter(status='Ready')


def get_manager_contracts(user):
    successful_leads = user.studyrequest_set.filter(status='Ready')
    return Contract.objects.filter(lead__in=successful_leads)


def get_manager_successful_contracts(user):
    successful_leads = user.studyrequest_set.filter(status='Ready')
    return Contract.objects.filter(lead__in=successful_leads, is_subscribed=True)


def get_manager_successful_lead_percent(user):
    """
    Calculate manager success leads percent
    :param user: AdvUser object
    :return: float percent result
    """
    leads_count = get_manager_leads(user).count()
    successful_contracts_count = get_manager_successful_contracts(user).count()

    if leads_count and successful_contracts_count:
        percent = round(successful_contracts_count / leads_count, 2) * 100
    else:
        percent = 0
    return percent


def get_manager_data_per_period(user, period_from=None, period_to=None):
    """
    Filter user leads and contract by date
    :param user: AdvUser object
    :param period_from: str date from
    :param period_to: str date to
    :return: dict contained leads and contracts of user
    """
    leads = get_manager_leads(user)
    successful_contracts = get_manager_successful_contracts(user)
    if period_from and period_to:
        data = [
            {
                'period': f'c {period_from} по {period_to}',
                'leads': leads.filter(enter_date__range=(period_from, period_to)),
                'successful_contracts': successful_contracts.filter(date__range=(period_from, period_to)),
            }
        ]
    elif period_from:
        data = [
            {
                'period': f'c {period_from}',
                'leads': leads.filter(enter_date__gte=period_from),
                'successful_contracts': successful_contracts.filter(date__gte=period_from),
            }
        ]
    elif period_to:
        data = [
            {
                'period': f'по {period_to}',
                'leads': leads.filter(enter_date__lte=period_to),
                'successful_contracts': successful_contracts.filter(date__lte=period_to),
            }
        ]
    else:
        data = [
        {
            'period': 'За всё время',
            'leads': leads,
            'successful_contracts': successful_contracts,
        },
        {
            'period': 'За год',
            'leads': leads.filter(enter_date__year=int(datetime.datetime.now().year)),
            'successful_contracts': successful_contracts.filter(date__year=int(datetime.datetime.now().year)),
        },
        {
            'period': 'За месяц',
            'leads': leads.filter(enter_date__month=int(datetime.datetime.now().month)),
            'successful_contracts': successful_contracts.filter(date__month=int(datetime.datetime.now().month)),
        },
        {
            'period': 'Прошедшие 7 дней',
            'leads': leads.filter(enter_date__gt=datetime.datetime.now() - datetime.timedelta(days=7)),
            'successful_contracts': successful_contracts.filter(date__gt=datetime.datetime.now() - datetime.timedelta(days=7)),
        },
        {
            'period': 'Сегодня',
            'leads': leads.filter(enter_date__day=int(datetime.datetime.now().day)),
            'successful_contracts': successful_contracts.filter(date__day=int(datetime.datetime.now().day)),
        }
    ]
    return data


def get_planning_rooms():
    rooms = Classroom.objects.all()
    date_set = []
    for i in range(60, 0, -1):
        date = datetime.date.today() - datetime.timedelta(days=i)
        date_set.append(date)
    for i in range(60):
        date = datetime.date.today() + datetime.timedelta(days=i)
        date_set.append(date)
    context = {
        'rooms': rooms,
        'date_set': date_set,
    }
    return context


def create_group_classes(request, count_days, group):
    if 'classes_days' in request.POST and 'class_room' in request.POST:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        days_list = [int(day) for day in request.POST.getlist('classes_days')]
        position = 1
        class_room = get_object_or_404(Classroom, title=request.POST["class_room"])
        for day in range(count_days.days + 1):
            dt = group.course.start_date + datetime.timedelta(day)
            if dt.weekday() in days_list:
                ClassModel.objects.create(
                    position=position,
                    theme=f'Тема-{position}',
                    groups=group,
                    classroom=class_room,
                    date=dt,
                    start_time=start_time,
                    end_time=end_time
                )
                position += 1
        return True
    return False
