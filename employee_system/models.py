from django.db import models

class EmployeeProfile(models.Model):
    STATUS_CHOICES = [('active','Active'),('pending','Pending'),('inactive','Inactive')]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=120)
    source_application_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    def __str__(self): return f'{self.first_name} {self.last_name}'
