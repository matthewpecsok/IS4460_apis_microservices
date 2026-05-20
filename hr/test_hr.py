from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from .models import JobPosting, CandidateApplication, HRReviewNote

class HRPermissionAndAPITests(TestCase):
    def setUp(self):
        self.hr_group = Group.objects.create(name='HR')
        self.hr_user = User.objects.create_user('hr_user', password='password123')
        self.hr_user.groups.add(self.hr_group)
        self.job = JobPosting.objects.create(title='Analyst', department='Finance', description='Test', status='approved', created_by=self.hr_user)

    def test_jobposting_str(self):
        self.assertEqual(str(self.job), 'Analyst (approved)')

    def test_candidate_application_str(self):
        application = CandidateApplication.objects.create(
            job=self.job, candidate_name='Taylor Candidate', candidate_email='taylor@example.com', resume_text='Resume text'
        )
        self.assertEqual(str(application), 'Taylor Candidate for Analyst')

    def test_hr_review_note_str(self):
        application = CandidateApplication.objects.create(
            job=self.job, candidate_name='Taylor Candidate', candidate_email='taylor@example.com', resume_text='Resume text'
        )
        note = HRReviewNote.objects.create(application=application, reviewer=self.hr_user, note='Looks good')
        self.assertEqual(str(note), f'Note for {application}')

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

    def test_hr_api_rejects_bad_token(self):
        response = self.client.post(reverse('hr:receive_application_api'), data={
            'hr_job_id': self.job.id, 'candidate_name': 'Taylor Candidate', 'candidate_email': 'taylor@example.com', 'resume_text': 'Resume text'
        }, content_type='application/json', HTTP_AUTHORIZATION='Token bad')
        self.assertEqual(response.status_code, 403)

    def test_hr_api_returns_404_for_missing_job(self):
        response = self.client.post(reverse('hr:receive_application_api'), data={
            'hr_job_id': 9999, 'candidate_name': 'Taylor Candidate', 'candidate_email': 'taylor@example.com', 'resume_text': 'Resume text'
        }, content_type='application/json', HTTP_AUTHORIZATION='Token class-hr-token')
        self.assertEqual(response.status_code, 404)

    def test_approved_jobs_api_returns_approved_and_published_jobs_only(self):
        JobPosting.objects.create(title='Draft Role', department='Sales', description='Draft', status='draft', created_by=self.hr_user)
        JobPosting.objects.create(title='Published Role', department='Sales', description='Live', status='published', created_by=self.hr_user)
        response = self.client.get(reverse('hr:approved_jobs_api'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        statuses = {job['status'] for job in data}
        self.assertIn('approved', statuses)
        self.assertIn('published', statuses)
        self.assertNotIn('draft', statuses)
