from django.contrib import admin
from .models import ExternalApplication, ExternalJobPosting

@admin.register(ExternalJobPosting)
class ExternalJobPostingAdmin(admin.ModelAdmin):
    list_display = ('title','department','status','hr_job_id','received_at')
    search_fields = ('title','department','description')

@admin.register(ExternalApplication)
class ExternalApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate_name','candidate_email','external_job','sent_to_hr','hr_application_id','submitted_at')
    list_filter = ('sent_to_hr',)
