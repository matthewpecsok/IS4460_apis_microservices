from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from .models import JobPosting, CandidateApplication

class HRPermissionAndAPITests(TestCase):
    def setUp(self):
        self.hr_group = Group.objects.create(name='HR')
        self.hr_user = User.objects.create_user('hr_user', password='password123')
        self.hr_user.groups.add(self.hr_group)
        self.job = JobPosting.objects.create(title='Analyst', department='Finance', description='Test', status='approved', created_by=self.hr_user)

    def test_anonymous_cannot_access_hr_dashboard(self):
        response = self.client.get(reverse('hr:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_hr_user_can_access_hr_dashboard(self):
        self.client.login(username='hr_user', password='password123')
        response = self.client.get(reverse('hr:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_hr_api_receives_application_with_correct_token(self):
        response = self.client.post(reverse('hr:receive_application_api'), data={
            'hr_job_id': self.job.id, 'candidate_name': 'Taylor Candidate', 'candidate_email': 'taylor@example.com', 'resume_text': 'Resume text'
        }, content_type='application/json', HTTP_AUTHORIZATION='Token class-hr-token')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CandidateApplication.objects.count(), 1)
