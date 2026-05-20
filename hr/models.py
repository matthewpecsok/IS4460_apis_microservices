from django.conf import settings
from django.db import models

class JobPosting(models.Model):
    STATUS_CHOICES = [('draft','Draft'),('approved','Approved'),('published','Published'),('closed','Closed')]
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=120)
    short_prompt = models.TextField(blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_posting_id = models.IntegerField(null=True, blank=True)
    def __str__(self): return f'{self.title} ({self.status})'

class CandidateApplication(models.Model):
    STATUS_CHOICES = [('submitted','Submitted'),('under_review','Under Review'),('interview','Interview'),('rejected','Rejected'),('hired','Hired')]
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    candidate_name = models.CharField(max_length=200)
    candidate_email = models.EmailField()
    resume_text = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    source_system = models.CharField(max_length=100, default='external_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f'{self.candidate_name} for {self.job.title}'

class HRReviewNote(models.Model):
    application = models.ForeignKey(CandidateApplication, on_delete=models.CASCADE, related_name='notes')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Note for {self.application}'
