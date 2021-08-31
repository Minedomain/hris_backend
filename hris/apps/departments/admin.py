from django.contrib import admin

from .models import *

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["department_id", "department_name", "department_details"]
