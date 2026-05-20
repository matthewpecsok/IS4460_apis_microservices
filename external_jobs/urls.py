from django.urls import path
from . import views
app_name = 'external_jobs'
urlpatterns = [
    path('', views.public_job_list, name='public_job_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:pk>/', views.public_job_detail, name='public_job_detail'),
    path('<int:pk>/apply/', views.apply, name='apply'),
    path('applications/<int:pk>/confirmation/', views.application_confirmation, name='application_confirmation'),
    path('api/job-postings/', views.receive_job_posting_api, name='receive_job_posting_api'),
    path('api/job-postings/list/', views.list_job_postings_api, name='list_job_postings_api'),
]
