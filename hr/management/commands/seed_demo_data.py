from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from hr.models import CandidateApplication, JobPosting
from external_jobs.models import ExternalApplication, ExternalJobPosting
from employee_system.models import EmployeeProfile

class Command(BaseCommand):
    help = 'Create groups, sample users, jobs, applications, and employees for the teaching demo.'

    def handle(self, *args, **options):
        hr_group, _ = Group.objects.get_or_create(name='HR')
        emp_group, _ = Group.objects.get_or_create(name='EmployeeSystem')
        hr_user, _ = User.objects.get_or_create(username='hr_user', defaults={'email':'hr@example.com'})
        hr_user.set_password('password123'); hr_user.save(); hr_user.groups.add(hr_group)
        emp_user, _ = User.objects.get_or_create(username='employee_user', defaults={'email':'employee@example.com'})
        emp_user.set_password('password123'); emp_user.save(); emp_user.groups.add(emp_group)
        admin, _ = User.objects.get_or_create(username='admin', defaults={'email':'admin@example.com', 'is_staff':True, 'is_superuser':True})
        admin.is_staff = True; admin.is_superuser = True; admin.set_password('password123'); admin.save()
        job, _ = JobPosting.objects.get_or_create(
            title='Junior Data Analyst', department='Finance',
            defaults={'short_prompt':'Create a junior data analyst job posting for finance. Emphasize Excel, communication, and willingness to learn.', 'description':'Sample approved analyst posting.', 'status':'approved', 'created_by':hr_user})
        ext_job, _ = ExternalJobPosting.objects.get_or_create(hr_job_id=job.id, defaults={'title':job.title,'department':job.department,'description':job.description,'status':'open'})
        app, _ = CandidateApplication.objects.get_or_create(job=job, candidate_email='casey@example.com', defaults={'candidate_name':'Casey Rivera','resume_text':'Excel, class projects, communication experience.','source_system':'external_jobs'})
        ExternalApplication.objects.get_or_create(external_job=ext_job, candidate_email='casey@example.com', defaults={'candidate_name':'Casey Rivera','resume_text':'Excel and analytics coursework.','sent_to_hr':True,'hr_application_id':app.id})
        EmployeeProfile.objects.get_or_create(email='alex.employee@example.com', defaults={'first_name':'Alex','last_name':'Employee','department':'Operations','status':'active'})
        self.stdout.write(self.style.SUCCESS('Demo data created. Password for all sample users: password123'))
