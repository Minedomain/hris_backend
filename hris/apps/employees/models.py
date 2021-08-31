from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
import uuid

def signature(instance, filename):
    return '/'.join( ['signatures', str(instance.id), filename] )

def documents(instance, filename):
    return '/'.join( ['documents', str(instance.id), filename] )


class Employee(AbstractUser):
    MANAGER = 'Manager'
    HR = 'HR'
    NORMAL = 'Normal'
    DEPT_ROLE = [
        (MANAGER , _('Manager')),
        (HR , _('HR')),
        (NORMAL, _('Normal'))
    ]
    
    UNKNOWN = 'Unknown'
    REGULAR = 'Regular'
    CONTRACTUAL = 'Contractual'
    PROBATIONARY = 'Probationary'
    EMPLOYEE_STATUS = [
        (UNKNOWN, _('Unknown')),
        (REGULAR, _('Regular')),
        (CONTRACTUAL , _('Contractual')),
        (PROBATIONARY, _('Probationary'))
    ]

    employee_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    username = models.CharField(max_length=255, blank=False, unique=True)
    sa_no = models.CharField(max_length=255, blank=True, null=True, default=None)
    email = models.EmailField(max_length=255, blank=False, null=True, default=None)
    password = models.CharField(max_length=255)
    job_id = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, blank=True, null=True, default=None)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, default=None)
    department_id = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, blank=True, null=True, default=None)
    department_role = models.CharField(max_length=255, choices=DEPT_ROLE, default=NORMAL)
    company_id = models.ForeignKey('companies.Company', on_delete=models.SET_NULL, blank=True, null=True, default=None)
    date_employed = models.DateField(max_length=255, blank=True, null=True, default=None)
    employee_status = models.CharField(max_length=255, choices=EMPLOYEE_STATUS, default=UNKNOWN)
    salary = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0.00)
    sick_leave_count = models.IntegerField(validators=[MaxValueValidator(15)], null=True, default=0)
    vac_leave_count = models.IntegerField(validators=[MaxValueValidator(15)], null=True, default=0)
    name = models.CharField(max_length=255, blank=True, null=True, default=None)
    nickname = models.CharField(max_length=255, blank=True, null=True, default=None)
    other_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    employee_image = models.CharField(max_length=255, blank=True, null=True, default=None)
    civil_status = models.CharField(max_length=255, blank=True, null=True, default=None)
    citizenship = models.CharField(max_length=255, blank=True, null=True, default=None)
    gender = models.CharField(max_length=255, blank=True, null=True, default=None)
    weight = models.CharField(max_length=255, blank=True, null=True, default=None)
    height = models.CharField(max_length=255, blank=True, null=True, default=None)
    date_of_birth = models.DateField(max_length=255, blank=True, null=True, default=None)
    place_of_birth = models.CharField(max_length=255, blank=True, null=True, default=None)
    city_address = models.CharField(max_length=255, blank=True, null=True, default=None)
    prov_address = models.CharField(max_length=255, blank=True, null=True, default=None)
    tel_no = models.CharField(max_length=255, blank=True, null=True, default=None)
    cel_no = models.CharField(max_length=255, blank=True, null=True, default=None)
    religion = models.CharField(max_length=255, blank=True, null=True, default=None)
    acr_no = models.CharField(max_length=255, blank=True, null=True, default=None)
    acr_date = models.DateField(max_length=255, blank=True, null=True, default=None)
    dept_labor_no = models.CharField(max_length=255, blank=True,null=True, default=None)
    dept_labor_date = models.DateField(max_length=255, blank=True,null=True, default=None)
    tin_no = models.CharField(max_length=255, blank=True, null=True, default=None)
    sss_no = models.CharField(max_length=255, blank=True, null=True, default=None)
    pagibig_no = models.CharField(max_length=255, blank=True, null=True, default=None)
    philhealth_no = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return f" Employee: {self.username} {self.name}"

    def __init__(self, *args, **kwargs):
        super(Employee, self).__init__(*args, **kwargs)
        if self.is_superuser == True:
            self.is_staff = True
        else:
            self.is_staff = False

class EmployeeEducation(models.Model):
    educ_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.OneToOneField(Employee, on_delete=models.CASCADE)
    primary_school = models.CharField(max_length=255, blank=True, null=True, default=None)
    primary_address = models.CharField(max_length=255, blank=True, null=True, default=None)
    primary_grad = models.CharField(max_length=255, blank=True, null=True, default=None)
    sec_school = models.CharField(max_length=255, blank=True, null=True, default=None)
    sec_address = models.CharField(max_length=255, blank=True, null=True, default=None)
    sec_grad = models.CharField(max_length=255, blank=True, null=True, default=None)
    col_school = models.CharField(max_length=255, blank=True, null=True, default=None)
    col_address = models.CharField(max_length=255, blank=True, null=True, default=None)
    col_degree = models.CharField(max_length=255, blank=True, null=True, default=None)
    col_grad = models.CharField(max_length=255, blank=True, null=True, default=None)
    grad_school = models.CharField(max_length=255, blank=True, null=True, default=None)
    grad_address = models.CharField(max_length=255, blank=True, null=True, default=None)
    grad_degree = models.CharField(max_length=255, blank=True, null=True, default=None)
    grad_grad = models.CharField(max_length=255, blank=True, null=True, default=None)
    others = models.CharField(max_length=255, blank=True, null=True, default=None)

class EmployeeJobHistory(models.Model):
    job_history_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employer_name = models.CharField(max_length=255, blank=False)
    company_address = models.CharField(max_length=255, blank=True, null=True, default=None)
    company_contact_no = models.CharField(max_length=255, blank=True, null=True, default=None)
    company_supervisor = models.CharField(max_length=255, blank=True, null=True, default=None)
    job_title = models.CharField(max_length=255, blank=True, null=True, default=None)
    starting_income = models.IntegerField(blank=True, null=True, default=0)
    last_income = models.IntegerField(blank=True, null=True, default=0)
    reason_leave = models.CharField(max_length=255, blank=True, null=True, default=None)
    has_been_terminated = models.BooleanField(default=False)
    has_terminated_reason = models.CharField(max_length=255, blank=True, null=True, default=None)

class EmployeeExamsTaken(models.Model):
    exam_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=255, blank=False)
    date_taken = models.DateField(max_length=255, blank=False)
    result = models.CharField(max_length=255, blank=False)

class EmployeeSeminarsTaken(models.Model):
    seminar_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    seminar_name = models.CharField(max_length=255, blank=False)
    seminar_date = models.DateField(max_length=255, blank=False)

class EmployeeSkills(models.Model):
    skill_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255, blank=True, null=True, default=None)

class EmployeeFamily(models.Model):
    family_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.OneToOneField(Employee, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=255, blank=False)
    father_birth = models.DateField(max_length=255, blank=True, null=True, default=None)
    father_age = models.IntegerField(blank=True, null=True, default=None)
    father_occu = models.CharField(max_length=255, blank=True, null=True, default=None)
    father_employer = models.CharField(max_length=255, blank=True, null=True, default=None)
    mother_name = models.CharField(max_length=255, blank=False)
    mother_birth = models.DateField(max_length=255, blank=True, null=True, default=None)
    mother_age = models.IntegerField(blank=True, null=True, default=None)
    mother_occu = models.CharField(max_length=255, blank=True, null=True, default=None)
    mother_employer = models.CharField(max_length=255, blank=True, null=True, default=None)
    family_address = models.CharField(max_length=255, blank=True, null=True, default=None)
    family_contact_no = models.CharField(max_length=255, blank=True, null=True, default=None)

class EmployeeSibling(models.Model):
    sibling_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    sibling_name = models.CharField(max_length=255, blank=False)
    sibling_age = models.IntegerField(blank=True, null=True, default=None)
    sibling_occupation = models.CharField(max_length=255, blank=True, null=True, default=None)
    sibling_employer = models.CharField(max_length=255, blank=True, null=True, default=None)

class EmployeeMarried(models.Model):
    married_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.OneToOneField(Employee, on_delete=models.CASCADE)
    spouse_name = models.CharField(max_length=255, blank=False)
    spouse_address = models.CharField(max_length=255, blank=True, null=True, default=None)
    spouse_birth = models.DateField(max_length=255, blank=True, null=True, default=None)
    spouse_age = models.IntegerField(blank=True, null=True, default=None)
    spouse_occupation = models.CharField(max_length=255, blank=True, null=True, default=None)
    spouse_employer = models.CharField(max_length=255, blank=True, null=True, default=None)

class EmployeeChildren(models.Model):
    child_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    child_name = models.CharField(max_length=255, blank=False)
    child_age = models.IntegerField(blank=True, null=True, default=None)

class EmployeeMedicalHistory(models.Model):
    med_history_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.OneToOneField(Employee, on_delete=models.CASCADE, unique=True)
    had_illness = models.BooleanField(default=False)
    illness_details = models.CharField(max_length=255, blank=True, null=True, default=None)
    hospitalized = models.BooleanField(default=False)
    hospitalized_details = models.CharField(max_length=255, blank=True, null=True, default=None)
    last_checkup_purpose = models.CharField(max_length=255, blank=True, null=True, default=None)
    last_checkup_place = models.CharField(max_length=255, blank=True, null=True, default=None)
    last_checkup_date = models.DateField(max_length=255, blank=True, null=True, default=None)
    distinguishing_marks = models.CharField(max_length=255, blank=True, null=True, default=None)

class EmployeeReference(models.Model):
    ref_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    ref_name = models.CharField(max_length=255, blank=False)
    ref_occupation = models.CharField(max_length=255, blank=True, null=True, default=None)
    ref_employer = models.CharField(max_length=255, blank=True, null=True, default=None)

class EmployeeOrganization(models.Model):
    org_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=255, blank=False)
    org_desc = models.CharField(max_length=255, blank=True, null=True, default=None)

class EmployeeOffense(models.Model):
    offense_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.OneToOneField(Employee, on_delete=models.CASCADE, unique=True)
    convicted = models.BooleanField(default=False)
    offense_details = models.CharField(max_length=255, blank=True, null=True, default=None)
    offense_court = models.CharField(max_length=255, blank=True, null=True, default=None)
    date_filed = models.DateField(max_length=255, blank=True, null=True, default=None)
    termination_record = models.BooleanField(default=False)
    revocation_record = models.BooleanField(default=False)
    injunction_record = models.BooleanField(default=False)
    arrest_record = models.BooleanField(default=False)

class EmployeeEmergency(models.Model):
    emergency_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.OneToOneField(Employee, on_delete=models.CASCADE, unique=True)
    person_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    person_relationship = models.CharField(max_length=255, blank=True, null=True, default=None)
    person_address = models.CharField(max_length=255, blank=True, null=True, default=None)
    person_phone = models.CharField(max_length=255, blank=True, null=True, default=None)

class EmployeeSignature(models.Model):
    signature_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.OneToOneField(Employee, on_delete=models.CASCADE, unique=True)
    employee_signature = models.ImageField(upload_to=signature, max_length=255, blank=False)

class EmployeeDocuments(models.Model):
    docu_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    docu_name = models.CharField(max_length=255, blank=False)
    docu_details = models.CharField(max_length=255, blank=True, null=True, default=None)
    docu_date_created = models.DateField(max_length=255, blank=True, null=True, default=None)
    docu_date_uploaded = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    docu_file_url = models.ImageField(upload_to=documents, max_length=255, blank=False)
