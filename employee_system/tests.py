from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from .models import EmployeeProfile

class EmployeeSystemTests(TestCase):
    def setUp(self):
        group = Group.objects.create(name='EmployeeSystem')
        user = User.objects.create_user('employee_user', password='password123')
        user.groups.add(group)

    def test_employee_user_can_access_employee_dashboard(self):
        self.client.login(username='employee_user', password='password123')
        response = self.client.get(reverse('employee_system:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_employee_system_api_creates_employee_with_correct_token(self):
        response = self.client.post(reverse('employee_system:create_employee_api'), data={
            'first_name': 'Jordan', 'last_name': 'Hire', 'email': 'jordan@example.com', 'department': 'Finance', 'source_application_id': 1, 'status': 'active'
        }, content_type='application/json', HTTP_AUTHORIZATION='Token class-employee-system-token')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(EmployeeProfile.objects.count(), 1)

    def test_employee_system_api_rejects_unauthorized_requests(self):
        response = self.client.post(reverse('employee_system:create_employee_api'), data={'email':'bad@example.com'}, content_type='application/json', HTTP_AUTHORIZATION='Token bad')
        self.assertEqual(response.status_code, 403)
