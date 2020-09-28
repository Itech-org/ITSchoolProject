from functools import wraps
from urllib.parse import urlparse
import random

# from .models import Contract

from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.shortcuts import resolve_url, get_object_or_404
from Main_project_school import settings
from django.template.loader import render_to_string
from django.core.signing import Signer
from Main_project_school.settings import ALLOWED_HOSTS
from django.template.defaultfilters import slugify as django_slugify


alphabet = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
    'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
    'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
    'я': 'ya'
}


def slugify(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))

signer = Signer()


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


def send_password(user, password):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {
        'user': user,
        'host': host,
        'sign': signer.sign(user.username),
        'password': password
    }
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)


def check_group_and_activation(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Manager").exists():
            return True
        else:
            logout(request)
            return False
    else:
        return False


def apply_group_settings(request, group):
    title = request.POST.get('title', '')
    teacher = AvdUser.objects.get(first_name=request.POST.get('teacher', ''))
    manager = request.POST.get('manager', '')
    postponed = request.POST.get('postponed', '')
    if title != group.title:
        group.title = title
    if teacher != group.teacher:
        group.teacher = teacher
    if manager != group.manager:
        group.manager = manager
    if postponed:
        group.course_postponation(postponed)
    group.save()
    return True