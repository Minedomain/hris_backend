# Generated by Django 2.2.16 on 2021-06-18 08:20

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('jobs', '0001_initial'),
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('employee_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('sa_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('email', models.EmailField(default=None, max_length=255, null=True)),
                ('password', models.CharField(max_length=255)),
                ('date_employed', models.DateField(blank=True, default=None, max_length=255, null=True)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('vac_leave_count', models.IntegerField(default=0, null=True, validators=[django.core.validators.MaxValueValidator(15)])),
                ('sick_leave_count', models.IntegerField(default=0, null=True, validators=[django.core.validators.MaxValueValidator(15)])),
                ('name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('nickname', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('other_name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_image', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('civil_status', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('citizenship', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('weight', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('height', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('date_of_birth', models.DateField(blank=True, default=None, max_length=255, null=True)),
                ('place_of_birth', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('city_address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('prov_address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('tel_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('cel_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('religion', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('acr_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('acr_date', models.DateField(blank=True, default=None, max_length=255, null=True)),
                ('dept_labor_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('dept_labor_date', models.DateField(blank=True, default=None, max_length=255, null=True)),
                ('tin_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('sss_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('pagibig_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('philhealth_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('department_id', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='departments.Department')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('job_id', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.Job')),
                ('supervisor', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('skill_name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeSignature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('employee_signature', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeSibling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sibling_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('sibling_name', models.CharField(max_length=255)),
                ('sibling_age', models.IntegerField(blank=True, default=None, null=True)),
                ('sibling_occupation', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('sibling_employer', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeSeminarsTaken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seminar_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('seminar_name', models.CharField(max_length=255)),
                ('seminar_date', models.DateField(max_length=255)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('ref_name', models.CharField(max_length=255)),
                ('ref_occupation', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('ref_employer', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeOrganization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('org_name', models.CharField(max_length=255)),
                ('org_desc', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeOffense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offense_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('convicted', models.BooleanField(default=False)),
                ('offense_details', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('offense_court', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('date_filed', models.DateField(blank=True, default=None, max_length=255, null=True)),
                ('termination_record', models.BooleanField(default=False)),
                ('revocation_record', models.BooleanField(default=False)),
                ('injunction_record', models.BooleanField(default=False)),
                ('arrest_record', models.BooleanField(default=False)),
                ('employee_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeMedicalHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('med_history_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('had_illness', models.BooleanField(default=False)),
                ('illness_details', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('hospitalized', models.BooleanField(default=False)),
                ('hospitalized_details', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('last_checkup_purpose', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('last_checkup_place', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('last_checkup_date', models.DateField(blank=True, default=None, max_length=255, null=True)),
                ('distinguishing_marks', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeMarried',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('married_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('spouse_name', models.CharField(max_length=255)),
                ('spouse_address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('spouse_birth', models.DateField(blank=True, default=None, max_length=255, null=True)),
                ('spouse_age', models.IntegerField(blank=True, default=None, null=True)),
                ('spouse_occupation', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('spouse_employer', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeJobHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_history_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('employer_name', models.CharField(max_length=255)),
                ('company_address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('company_contact_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('company_supervisor', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('job_title', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('starting_income', models.IntegerField(blank=True, default=0, null=True)),
                ('last_income', models.IntegerField(blank=True, default=0, null=True)),
                ('reason_leave', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('has_been_terminated', models.BooleanField(default=False)),
                ('has_terminated_reason', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('father_name', models.CharField(max_length=255)),
                ('father_birth', models.DateField(blank=True, default=None, max_length=255, null=True)),
                ('father_age', models.IntegerField(blank=True, default=None, null=True)),
                ('father_occu', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('father_employer', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('mother_name', models.CharField(max_length=255)),
                ('mother_birth', models.DateField(blank=True, default=None, max_length=255, null=True)),
                ('mother_age', models.IntegerField(blank=True, default=None, null=True)),
                ('mother_occu', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('mother_employer', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('family_address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('family_contact_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeExamsTaken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('exam_name', models.CharField(max_length=255)),
                ('date_taken', models.DateField(max_length=255)),
                ('result', models.CharField(max_length=255)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeEmergency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emergency_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('person_name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('person_relationship', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('person_address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('person_phone', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('educ_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('primary_school', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('primary_address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('primary_grad', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('sec_school', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('sec_address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('sec_grad', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('col_school', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('col_address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('col_degree', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('col_grad', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('grad_school', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('grad_address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('grad_degree', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('grad_grad', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('others', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('employee_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docu_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('docu_name', models.CharField(max_length=255)),
                ('docu_details', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('docu_date_created', models.DateField(blank=True, default=None, max_length=255, null=True)),
                ('docu_date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('docu_file_url', models.CharField(max_length=255)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeChildren',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('child_name', models.CharField(max_length=255)),
                ('child_age', models.IntegerField(blank=True, default=None, null=True)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
