from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def is_employee_system_user(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='EmployeeSystem').exists())


def employee_system_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_employee_system_user(request.user):
            raise PermissionDenied('EmployeeSystem group membership is required.')
        return view_func(request, *args, **kwargs)
    return wrapper
