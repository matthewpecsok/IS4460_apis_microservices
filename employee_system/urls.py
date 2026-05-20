from django.urls import path
from . import views
app_name = 'employee_system'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('api/employees/', views.create_employee_api, name='create_employee_api'),
]
