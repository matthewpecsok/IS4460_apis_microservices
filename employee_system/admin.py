from django.contrib import admin
from .models import EmployeeProfile

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','department','status','source_application_id','created_at')
    list_filter = ('status','department')
    search_fields = ('first_name','last_name','email','department')
