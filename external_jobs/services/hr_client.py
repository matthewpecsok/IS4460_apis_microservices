import os
import requests
from django.conf import settings


def send_application_to_hr(application):
    """Send candidate data back to HR through the HR API.

    This intentionally uses a simple static token for class readability. Real
    external partners should use stronger authentication and rate limiting.
    """
    url = settings.BASE_URL.rstrip('/') + '/hr/api/applications/'
    token = os.getenv('HR_API_TOKEN', settings.HR_API_TOKEN)
    payload = {
        'hr_job_id': application.external_job.hr_job_id,
        'candidate_name': application.candidate_name,
        'candidate_email': application.candidate_email,
        'resume_text': application.resume_text,
        'source_system': 'external_jobs',
    }
    response = requests.post(url, json=payload, headers={'Authorization': f'Token {token}'}, timeout=10)
    response.raise_for_status()
    return response.json()
