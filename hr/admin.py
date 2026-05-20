from django.contrib import admin
from .models import CandidateApplication, HRReviewNote, JobPosting

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title','department','status','external_posting_id','created_by','updated_at')
    list_filter = ('status','department')
    search_fields = ('title','department','description')

@admin.register(CandidateApplication)
class CandidateApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate_name','candidate_email','job','status','source_system','created_at')
    list_filter = ('status','source_system')
    search_fields = ('candidate_name','candidate_email','resume_text')

@admin.register(HRReviewNote)
class HRReviewNoteAdmin(admin.ModelAdmin):
    list_display = ('application','reviewer','created_at')
