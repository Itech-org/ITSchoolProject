import datetime
from .models import Contract


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


def get_manager_successful_percent(user, model):
    if model == 'StudyRequest':
        successful_count = get_manager_successful_leads(user).count()
        count = get_manager_leads(user).count()
    elif model == 'Contract':
        successful_count = get_manager_successful_contracts(user).count()
        count = get_manager_contracts(user).count()
    else:
        successful_count = 0
        count = 0
    if successful_count == 0 or count == 0:
        percent = 0
    else:
        percent = round(successful_count / count, 2) * 100
    return percent


def get_manager_data_per_period(user):
    leads = get_manager_leads(user)
    successful_leads = get_manager_successful_leads(user)
    contracts = get_manager_contracts(user)
    successful_contracts = get_manager_successful_contracts(user)
    data = [
        {
            'period': 'За всё время',
            'leads': leads,
            'successful_leads': successful_leads,
            'contracts': contracts,
            'successful_contracts': successful_contracts,
        },
        {
            'period': 'За год',
            'leads': leads.filter(enter_date__year=int(datetime.datetime.now().year)),
            'successful_leads': successful_leads.filter(enter_date__year=int(datetime.datetime.now().year)),
            'contracts': contracts.filter(date__year=int(datetime.datetime.now().year)),
            'successful_contracts': successful_contracts.filter(date__year=int(datetime.datetime.now().year)),
        },
        {
            'period': 'За месяц',
            'leads': leads.filter(enter_date__month=int(datetime.datetime.now().month)),
            'successful_leads': successful_leads.filter(enter_date__month=int(datetime.datetime.now().month)),
            'contracts': contracts.filter(date__month=int(datetime.datetime.now().month)),
            'successful_contracts': successful_contracts.filter(date__month=int(datetime.datetime.now().month)),
        },
        {
            'period': 'Прошедшие 7 дней',
            'leads': leads.filter(enter_date__gt=datetime.datetime.now() - datetime.timedelta(days=7)),
            'successful_leads': successful_leads.filter(enter_date__gt=datetime.datetime.now() - datetime.timedelta(days=7)),
            'contracts': contracts.filter(date__gt=datetime.datetime.now() - datetime.timedelta(days=7)),
            'successful_contracts': successful_contracts.filter(date__gt=datetime.datetime.now() - datetime.timedelta(days=7)),
        },
        {
            'period': 'Сегодня',
            'leads': leads.filter(enter_date__day=int(datetime.datetime.now().day)),
            'successful_leads': successful_leads.filter(enter_date__day=int(datetime.datetime.now().day)),
            'contracts': contracts.filter(date__day=int(datetime.datetime.now().day)),
            'successful_contracts': successful_contracts.filter(date__day=int(datetime.datetime.now().day)),
        }
    ]
    return data