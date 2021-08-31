from django.contrib import admin

from .models import *

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['leave_id', 'employee_id', 'leave_type', 'leave_reason', 'date_filed', 'leave_status']
