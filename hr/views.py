from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .forms import CandidateStatusForm, HRReviewNoteForm, JobPostingForm
from .models import CandidateApplication, JobPosting
from .permissions import hr_required
from .services.employee_system_client import create_employee_from_application
from .services.external_jobs_client import publish_job_to_external_site
from .services.gemini_service import generate_job_description


def _valid_token(request, expected):
    # Teaching simplification only. Real systems should use stronger auth.
    auth = request.headers.get('Authorization', '')
    return auth == f'Token {expected}'

@hr_required
def dashboard(request):
    return render(request, 'hr/dashboard.html', {
        'job_count': JobPosting.objects.count(),
        'application_count': CandidateApplication.objects.count(),
        'hired_count': CandidateApplication.objects.filter(status='hired').count(),
    })

@hr_required
def job_list(request):
    return render(request, 'hr/job_list.html', {'jobs': JobPosting.objects.order_by('-created_at')})

@hr_required
def job_create(request):
    form = JobPostingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        job = form.save(commit=False)
        job.created_by = request.user
        job.save()
        messages.success(request, 'Job posting created.')
        return redirect('hr:job_detail', pk=job.pk)
    return render(request, 'hr/job_form.html', {'form': form, 'title': 'Create Job Posting'})

@hr_required
def job_edit(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    form = JobPostingForm(request.POST or None, instance=job)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Job posting updated.')
        return redirect('hr:job_detail', pk=job.pk)
    return render(request, 'hr/job_form.html', {'form': form, 'title': 'Edit Job Posting'})

@hr_required
def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    return render(request, 'hr/job_detail.html', {'job': job})

@hr_required
@require_POST
def generate_description(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    job.description = generate_job_description(job.short_prompt or job.title)
    job.save()
    messages.success(request, 'Draft description generated.')
    return redirect('hr:job_detail', pk=pk)

@hr_required
@require_POST
def approve_job(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    job.status = 'approved'
    job.save()
    messages.success(request, 'Job approved.')
    return redirect('hr:job_detail', pk=pk)

@hr_required
@require_POST
def publish_job(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    if job.status not in ['approved', 'published']:
        messages.error(request, 'Only approved jobs can be published.')
        return redirect('hr:job_detail', pk=pk)
    try:
        data = publish_job_to_external_site(job)
        job.external_posting_id = data.get('id')
        job.status = 'published'
        job.save()
        messages.success(request, 'Job sent to external job site API.')
    except Exception as exc:
        messages.error(request, f'Could not publish job. Is the server running? {exc}')
    return redirect('hr:job_detail', pk=pk)

@hr_required
def application_list(request):
    return render(request, 'hr/application_list.html', {'applications': CandidateApplication.objects.select_related('job').order_by('-created_at')})

@hr_required
def application_detail(request, pk):
    app = get_object_or_404(CandidateApplication.objects.select_related('job'), pk=pk)
    status_form = CandidateStatusForm(request.POST or None, instance=app)
    note_form = HRReviewNoteForm()
    if request.method == 'POST' and 'update_status' in request.POST and status_form.is_valid():
        status_form.save()
        messages.success(request, 'Candidate status updated.')
        return redirect('hr:application_detail', pk=pk)
    if request.method == 'POST' and 'add_note' in request.POST:
        note_form = HRReviewNoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.application = app
            note.reviewer = request.user
            note.save()
            messages.success(request, 'Review note added.')
            return redirect('hr:application_detail', pk=pk)
    return render(request, 'hr/application_detail.html', {'application': app, 'status_form': status_form, 'note_form': note_form})

@hr_required
@require_POST
def hire_candidate(request, pk):
    app = get_object_or_404(CandidateApplication, pk=pk)
    app.status = 'hired'
    app.save()
    try:
        create_employee_from_application(app)
        messages.success(request, 'Candidate hired and sent to employee system API.')
    except Exception as exc:
        messages.error(request, f'Candidate marked hired, but employee API call failed. {exc}')
    return redirect('hr:application_detail', pk=pk)

@api_view(['POST'])
def receive_application_api(request):
    if not _valid_token(request, settings.HR_API_TOKEN):
        return Response({'detail': 'Invalid HR API token.'}, status=status.HTTP_403_FORBIDDEN)
    try:
        job = JobPosting.objects.get(pk=request.data.get('hr_job_id'))
    except JobPosting.DoesNotExist:
        return Response({'detail': 'HR job not found.'}, status=status.HTTP_404_NOT_FOUND)
    app = CandidateApplication.objects.create(
        job=job,
        candidate_name=request.data.get('candidate_name',''),
        candidate_email=request.data.get('candidate_email',''),
        resume_text=request.data.get('resume_text',''),
        source_system=request.data.get('source_system','external_jobs'),
    )
    return Response({'id': app.id, 'status': app.status}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def approved_jobs_api(request):
    jobs = JobPosting.objects.filter(status__in=['approved','published']).values('id','title','department','description','status')
    return Response(list(jobs))
