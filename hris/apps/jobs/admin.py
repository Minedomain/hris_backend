from django.contrib import admin

from .models import *

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['job_id', 'job_title', 'duties', 'min_salary', 'max_salary']
