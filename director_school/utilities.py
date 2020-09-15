from functools import wraps
from urllib.parse import urlparse

from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.shortcuts import resolve_url

from manager_school.models import RequestConversation, Contract


def user_passes_test_custom(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator


def check_group_and_activation(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Director").exists():
            return True
        else:
            logout(request)
            return False
    else:
        return False


def get_requests(managers):
    requests = {}
    for manager in managers:
        requests_count = manager.studyrequest_set.all().count()
        requests_ready = manager.studyrequest_set.filter(status="Ready").count()
        requests_ip = manager.studyrequest_set.filter(status="In Progress").count()
        requests_denied = manager.studyrequest_set.filter(status="Denial").count()
        manager_dict = {
            'requests_count':requests_count,
            'requests_ready':requests_ready,
            'requests_ip':requests_ip,
            'requests_denied':requests_denied,
        }
        requests.update({manager.id:manager_dict})
    return requests


def get_conversations(managers):
    conversations = {}
    for manager in managers:
        conversations_all = RequestConversation.objects.filter(request__specialist=manager)
        count = conversations_all.count()
        ready = conversations_all.filter(status="Ready").count()
        call_back = conversations_all.filter(status="Call back").count()
        denied = conversations_all.filter(status="Denial").count()
        manager_dict = {
            'count':count,
            'ready':ready,
            'call_back':call_back,
            'denied':denied,
        }
        conversations.update({manager.id:manager_dict})
    return conversations


def get_contracts(managers):
    contracts = {}
    for manager in managers:
        contracts_all = Contract.objects.filter(lead__specialist=manager)
        count = contracts_all.count()
        subscribed = contracts_all.filter(is_subscribed=True).count()
        in_progress = contracts_all.filter(is_subscribed=False).count()
        manager_dict = {
            'count':count,
            'subscribed':subscribed,
            'in_progress':in_progress,
        }
        contracts.update({manager.id:manager_dict})
    return contracts


def get_user_payments(contracts):
    payments = {}
    for contract in contracts:
        payment = contract.payment
        stages = {}
        for stage in payment.paymentstage_set.all():
            if stage.is_confirmed:
                conf = 'Подтвержден'
            else:
                conf = 'Не подтвержден'
            if stage.picture:
                picture = stage.picture.url
            else:
                picture = 'Чек отсутствует'
            stage_dict = {
                'price':stage.price,
                'date':stage.date,
                'conf':conf,
                'picture':picture,
            }
            stages.update({stage.id:stage_dict})
        payments.update({contract.id:stages})
    return payments