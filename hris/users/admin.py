from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from hris.users.forms import UserChangeForm, UserCreationForm
from ..apps.employees.models import *

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        ("Employee", {"fields": ("sa_no", "email", "username", "supervisor", "job_id", "department_id", "department_role", "date_employed", 
                                "company_id", "salary", "employee_status")}),
        (_("Personal info"), {"fields": ("name","nickname", "other_name", "employee_image", "civil_status", "citizenship", "gender", 
                                        "weight", "height", "date_of_birth", "place_of_birth", "city_address", "prov_address",
                                        "tel_no", "cel_no", "religion", "acr_no", "acr_date", "dept_labor_no", "dept_labor_date",
                                        "tin_no", "sss_no", "pagibig_no", "philhealth_no")}),
        (_("Leave Count"), {"fields": ("sick_leave_count","vac_leave_count")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("date_joined",)}),
    )
    list_display = ["employee_id", "username", "name", "company_id", "department_id", "department_role", "employee_status", "is_superuser"]
    search_fields = ["name"]

@admin.register(EmployeeEducation)
class EmployeeEducationAdmin(admin.ModelAdmin):
    list_display = ['educ_id', 'employee_id', 'primary_school', 'primary_address', 'primary_grad', 'sec_school', 'sec_address', 'sec_grad',
        'col_school', 'col_address', 'col_degree', 'col_grad', 'grad_school', 'grad_address', 'grad_degree', 'grad_grad', 'others']

@admin.register(EmployeeJobHistory)
class EmployeeJobHistoryAdmin(admin.ModelAdmin):
    list_display = ['job_history_id', 'employee_id', 'employer_name', 'company_address', 'company_contact_no', 'company_supervisor',
    'job_title', 'starting_income', 'last_income', 'reason_leave', 'has_been_terminated', 'has_terminated_reason']

@admin.register(EmployeeExamsTaken)
class EmployeeExamsTakenAdmin(admin.ModelAdmin):
    list_display = ['exam_id', 'employee_id', 'exam_name', 'date_taken', 'result']

@admin.register(EmployeeSeminarsTaken)
class EmployeeSeminarsTakenAdmin(admin.ModelAdmin):
    list_display = ['seminar_id', 'employee_id', 'seminar_name', 'seminar_date']

@admin.register(EmployeeSkills)
class EmployeeSkillsAdmin(admin.ModelAdmin):
    list_display = ['skill_id', 'employee_id', 'skill_name']

@admin.register(EmployeeFamily)
class EmployeeFamilyAdmin(admin.ModelAdmin):
    list_display = ['family_id', 'employee_id', 'father_name', 'father_birth', 'father_age', 'father_occu', 'father_employer',
    'mother_name', 'mother_birth', 'mother_age', 'mother_occu', 'mother_employer', 'family_address', 'family_contact_no']

@admin.register(EmployeeSibling)
class EmployeeSiblingAdmin(admin.ModelAdmin):
    list_display = ['sibling_id', 'employee_id', 'sibling_name', 'sibling_age', 'sibling_occupation', 'sibling_employer']

@admin.register(EmployeeMarried)
class EmployeeMarriedAdmin(admin.ModelAdmin):
    list_display = ['married_id', 'employee_id', 'spouse_name', 'spouse_address', 'spouse_birth', 'spouse_age', 'spouse_occupation', 'spouse_employer']

@admin.register(EmployeeChildren)
class EmployeeChildrenAdmin(admin.ModelAdmin):
    list_display = ['child_id', 'employee_id', 'child_name', 'child_age']

@admin.register(EmployeeMedicalHistory)
class EmployeeMedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['med_history_id', 'employee_id', 'had_illness', 'illness_details', 'hospitalized', 'hospitalized_details', 'last_checkup_purpose',
    'last_checkup_place', 'last_checkup_date', 'distinguishing_marks']

@admin.register(EmployeeReference)
class EmployeeReferenceAdmin(admin.ModelAdmin):
    list_display = ['ref_id', 'employee_id', 'ref_name', 'ref_occupation', 'ref_employer']

@admin.register(EmployeeOrganization)
class EmployeeOrganizationAdmin(admin.ModelAdmin):
    list_display = ['org_id', 'employee_id', 'org_name', 'org_desc']

@admin.register(EmployeeOffense)
class EmployeeOffenseAdmin(admin.ModelAdmin):
    list_display = ['offense_id', 'employee_id', 'convicted', 'offense_details', 'offense_court', 'date_filed', 
    'termination_record', 'revocation_record', 'injunction_record', 'arrest_record']

@admin.register(EmployeeEmergency)
class EmployeeEmergencyAdmin(admin.ModelAdmin):
    list_display = ['emergency_id', 'employee_id', 'person_name', 'person_relationship', 'person_address', 'person_phone']

@admin.register(EmployeeSignature)
class EmployeeSignatureAdmin(admin.ModelAdmin):
    list_display = ['signature_id', 'employee_id', 'employee_signature']

@admin.register(EmployeeDocuments)
class EmployeeDocumentsAdmin(admin.ModelAdmin):
    list_display = ['docu_id', 'employee_id', 'docu_name', 'docu_details', 'docu_date_created', 'docu_date_uploaded', 'docu_file_url']