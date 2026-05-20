from django.test import TestCase
from django.urls import reverse
from .models import ExternalJobPosting, ExternalApplication

class ExternalJobsTests(TestCase):
    def test_external_job_posting_str(self):
        job = ExternalJobPosting.objects.create(hr_job_id=1, title='Analyst', department='Finance', description='Test', status='open')
        self.assertEqual(str(job), 'Analyst')

    def test_external_application_str(self):
        job = ExternalJobPosting.objects.create(hr_job_id=1, title='Analyst', department='Finance', description='Test', status='open')
        application = ExternalApplication.objects.create(
            external_job=job, candidate_name='Taylor Candidate', candidate_email='taylor@example.com', resume_text='Resume'
        )
        self.assertEqual(str(application), 'Taylor Candidate for Analyst')

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
        self.assertEqual(ExternalJobPosting.objects.count(), 1)

    def test_receive_job_posting_api_updates_existing_job(self):
        ExternalJobPosting.objects.create(hr_job_id=22, title='Developer', department='IS', description='Build apps', status='open')
        response = self.client.post(reverse('external_jobs:receive_job_posting_api'), data={
            'hr_job_id': 22, 'title': 'Developer II', 'department': 'IS', 'description': 'Updated build apps', 'status': 'open'
        }, content_type='application/json', HTTP_AUTHORIZATION='Token class-external-jobs-token')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExternalJobPosting.objects.count(), 1)
        job = ExternalJobPosting.objects.get(hr_job_id=22)
        self.assertEqual(job.title, 'Developer II')

    def test_list_job_postings_api_returns_all_jobs(self):
        ExternalJobPosting.objects.create(hr_job_id=1, title='Analyst', department='Finance', description='Test', status='open')
        ExternalJobPosting.objects.create(hr_job_id=2, title='Developer', department='IS', description='Build apps', status='open')
        response = self.client.get(reverse('external_jobs:list_job_postings_api'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual({job['hr_job_id'] for job in data}, {1, 2})

    def test_external_job_api_rejects_bad_token(self):
        response = self.client.post(reverse('external_jobs:receive_job_posting_api'), data={'hr_job_id': 1}, content_type='application/json', HTTP_AUTHORIZATION='Token bad')
        self.assertEqual(response.status_code, 403)
