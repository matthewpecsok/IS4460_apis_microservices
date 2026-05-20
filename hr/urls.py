from django.urls import path
from . import views
app_name = 'hr'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('jobs/<int:pk>/generate-description/', views.generate_description, name='generate_description'),
    path('jobs/<int:pk>/approve/', views.approve_job, name='approve_job'),
    path('jobs/<int:pk>/publish/', views.publish_job, name='publish_job'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/hire/', views.hire_candidate, name='hire_candidate'),
    path('api/applications/', views.receive_application_api, name='receive_application_api'),
    path('api/approved-jobs/', views.approved_jobs_api, name='approved_jobs_api'),
]
