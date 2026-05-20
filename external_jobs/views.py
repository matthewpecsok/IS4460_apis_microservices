from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .forms import ExternalApplicationForm
from .models import ExternalApplication, ExternalJobPosting
from .services.hr_client import send_application_to_hr


def _valid_token(request, expected):
    return request.headers.get('Authorization', '') == f'Token {expected}'

def public_job_list(request):
    jobs = ExternalJobPosting.objects.filter(status='open').order_by('-received_at')
    return render(request, 'external_jobs/public_job_list.html', {'jobs': jobs})

def public_job_detail(request, pk):
    job = get_object_or_404(ExternalJobPosting, pk=pk, status='open')
    return render(request, 'external_jobs/public_job_detail.html', {'job': job})

def apply(request, pk):
    job = get_object_or_404(ExternalJobPosting, pk=pk, status='open')
    form = ExternalApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        app = form.save(commit=False)
        app.external_job = job
        app.save()
        try:
            data = send_application_to_hr(app)
            app.sent_to_hr = True
            app.hr_application_id = data.get('id')
            app.save()
            return redirect('external_jobs:application_confirmation', pk=app.pk)
        except Exception as exc:
            messages.error(request, f'Application saved on external site, but HR API call failed. Is the server running? {exc}')
    return render(request, 'external_jobs/application_form.html', {'form': form, 'job': job})

def application_confirmation(request, pk):
    app = get_object_or_404(ExternalApplication, pk=pk)
    return render(request, 'external_jobs/application_confirmation.html', {'application': app})

@login_required
def dashboard(request):
    return render(request, 'external_jobs/dashboard.html', {
        'jobs': ExternalJobPosting.objects.order_by('-received_at'),
        'applications': ExternalApplication.objects.order_by('-submitted_at')[:20],
    })

@api_view(['POST'])
def receive_job_posting_api(request):
    if not _valid_token(request, settings.EXTERNAL_JOBS_API_TOKEN):
        return Response({'detail': 'Invalid external jobs API token.'}, status=status.HTTP_403_FORBIDDEN)
    job, _created = ExternalJobPosting.objects.update_or_create(
        hr_job_id=request.data.get('hr_job_id'),
        defaults={
            'title': request.data.get('title',''),
            'department': request.data.get('department',''),
            'description': request.data.get('description',''),
            'status': request.data.get('status','open'),
        }
    )
    return Response({'id': job.id, 'hr_job_id': job.hr_job_id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_job_postings_api(request):
    jobs = ExternalJobPosting.objects.values('id','hr_job_id','title','department','description','status')
    return Response(list(jobs))
