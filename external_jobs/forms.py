from django import forms
from .models import ExternalApplication

class ExternalApplicationForm(forms.ModelForm):
    class Meta:
        model = ExternalApplication
        fields = ['candidate_name','candidate_email','resume_text']
        widgets = {'resume_text': forms.Textarea(attrs={'rows':8})}
