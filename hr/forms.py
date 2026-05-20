from django import forms
from .models import CandidateApplication, HRReviewNote, JobPosting

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title','department','short_prompt','description','status']
        widgets = {'description': forms.Textarea(attrs={'rows':8}), 'short_prompt': forms.Textarea(attrs={'rows':3})}

class CandidateStatusForm(forms.ModelForm):
    class Meta:
        model = CandidateApplication
        fields = ['status']

class HRReviewNoteForm(forms.ModelForm):
    class Meta:
        model = HRReviewNote
        fields = ['note']
        widgets = {'note': forms.Textarea(attrs={'rows':3})}
