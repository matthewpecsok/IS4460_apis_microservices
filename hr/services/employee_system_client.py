import os
import requests
from django.conf import settings


def create_employee_from_application(application):
    url = settings.BASE_URL.rstrip('/') + '/employees/api/employees/'
    token = os.getenv('EMPLOYEE_SYSTEM_API_TOKEN', settings.EMPLOYEE_SYSTEM_API_TOKEN)
    parts = application.candidate_name.split()
    first_name = parts[0]
    last_name = ' '.join(parts[1:]) or 'Unknown'
    payload = {'first_name': first_name, 'last_name': last_name, 'email': application.candidate_email, 'department': application.job.department, 'source_application_id': application.id, 'status': 'active'}
    response = requests.post(url, json=payload, headers={'Authorization': f'Token {token}'}, timeout=10)
    response.raise_for_status()
    return response.json()
