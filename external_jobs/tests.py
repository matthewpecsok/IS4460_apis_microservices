from django.test import TestCase
from django.urls import reverse
from .models import ExternalJobPosting

class ExternalJobsTests(TestCase):
    def test_anonymous_can_view_public_job_listings(self):
        ExternalJobPosting.objects.create(hr_job_id=1, title='Analyst', department='Finance', description='Test', status='open')
        response = self.client.get(reverse('external_jobs:public_job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Analyst')

    def test_external_job_api_receives_job_with_correct_token(self):
        response = self.client.post(reverse('external_jobs:receive_job_posting_api'), data={
            'hr_job_id': 22, 'title': 'Developer', 'department': 'IS', 'description': 'Build apps', 'status': 'open'
        }, content_type='application/json', HTTP_AUTHORIZATION='Token class-external-jobs-token')
        self.assertEqual(response.status_code, 201)

    def test_external_job_api_rejects_bad_token(self):
        response = self.client.post(reverse('external_jobs:receive_job_posting_api'), data={'hr_job_id': 1}, content_type='application/json', HTTP_AUTHORIZATION='Token bad')
        self.assertEqual(response.status_code, 403)
