from django.db import models

class ExternalJobPosting(models.Model):
    hr_job_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(max_length=40, default='open')
    received_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class ExternalApplication(models.Model):
    external_job = models.ForeignKey(ExternalJobPosting, on_delete=models.CASCADE, related_name='applications')
    candidate_name = models.CharField(max_length=200)
    candidate_email = models.EmailField()
    resume_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    sent_to_hr = models.BooleanField(default=False)
    hr_application_id = models.IntegerField(null=True, blank=True)
    def __str__(self): return f'{self.candidate_name} for {self.external_job.title}'
