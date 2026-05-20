from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def is_hr_user(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='HR').exists())


def hr_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_hr_user(request.user):
            raise PermissionDenied('HR group membership is required.')
        return view_func(request, *args, **kwargs)
    return wrapper
