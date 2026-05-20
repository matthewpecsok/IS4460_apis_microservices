import os
import requests
from django.conf import settings


def publish_job_to_external_site(job):
    """Call the external job site's API.

    In production, system authentication would use OAuth, mTLS, signed JWTs, or
    another stronger mechanism. Static tokens are used here only for teaching.
    """
    url = settings.EXTERNAL_JOBS_BASE_URL.rstrip('/') + '/jobs/api/job-postings/'
    token = os.getenv('EXTERNAL_JOBS_API_TOKEN', settings.EXTERNAL_JOBS_API_TOKEN)
    payload = {'hr_job_id': job.id, 'title': job.title, 'department': job.department, 'description': job.description, 'status': 'open'}
    response = requests.post(url, json=payload, headers={'Authorization': f'Token {token}'}, timeout=10)
    response.raise_for_status()
    return response.json()
