import datetime
from .models import Contract, AdvUser


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