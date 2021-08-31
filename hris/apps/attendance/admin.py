from django.contrib import admin

from .models import *

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['attendance_id', 'employee_id', 'datetime_in', 'datetime_out', 'hours_logged', 'absent']
