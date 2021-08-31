from django.contrib import admin

from .models import *

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_id', 'company_name', 'company_description', 'company_address']

