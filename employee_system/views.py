from django.conf import settings
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EmployeeProfile
from .permissions import employee_system_required


def _valid_token(request, expected):
    return request.headers.get('Authorization', '') == f'Token {expected}'

@employee_system_required
def dashboard(request):
    return render(request, 'employee_system/dashboard.html', {'employee_count': EmployeeProfile.objects.count()})

@employee_system_required
def employee_list(request):
    return render(request, 'employee_system/employee_list.html', {'employees': EmployeeProfile.objects.order_by('last_name')})

@employee_system_required
def employee_detail(request, pk):
    employee = get_object_or_404(EmployeeProfile, pk=pk)
    return render(request, 'employee_system/employee_detail.html', {'employee': employee})

@api_view(['POST'])
def create_employee_api(request):
    if not _valid_token(request, settings.EMPLOYEE_SYSTEM_API_TOKEN):
        return Response({'detail': 'Invalid employee system API token.'}, status=status.HTTP_403_FORBIDDEN)
    employee, _created = EmployeeProfile.objects.update_or_create(
        email=request.data.get('email'),
        defaults={
            'first_name': request.data.get('first_name',''),
            'last_name': request.data.get('last_name',''),
            'department': request.data.get('department',''),
            'source_application_id': request.data.get('source_application_id'),
            'status': request.data.get('status','pending'),
        }
    )
    return Response({'id': employee.id, 'email': employee.email, 'status': employee.status}, status=status.HTTP_201_CREATED)
