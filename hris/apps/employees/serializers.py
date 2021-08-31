from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import *
from ..jobs.models import *
from ..departments.models import *

class EmployeeRegisterSerializer(serializers.ModelSerializer):
    
    employee_number = serializers.CharField(source='username')
    job_id = serializers.SlugRelatedField(slug_field='job_id', queryset=Job.objects.all(), allow_null=True)
    supervisor = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=True)
    department_id = serializers.SlugRelatedField(slug_field='department_id', queryset=Department.objects.all(), allow_null=True)

    class Meta:
        model = Employee
        fields = ['employee_id','employee_number', 'sa_no', 'email', 'job_id', 'supervisor', 'department_id', 'department_role', 'company_id', 'date_employed', 'employee_status', 
        'salary', 'sick_leave_count', 'vac_leave_count', 'name', 'nickname', 'other_name', 'employee_image', 'civil_status', 'citizenship', 'gender', 'weight', 'height', 
        'date_of_birth', 'place_of_birth', 'city_address', 'prov_address', 'tel_no', 'cel_no', 'religion', 'acr_no', 'acr_date', 'dept_labor_no', 'dept_labor_date',
        'tin_no', 'sss_no', 'pagibig_no', 'philhealth_no']

    def validate(self, data):
        username = data['username']
        sa_no = data['sa_no']
        email = data['email']
        date_of_birth = data['date_of_birth']
        errors = []

        # Check if employee number exists
        try:
            Employee.objects.get(username=username)
            errors.append('Employee number is already taken.')
        except Employee.DoesNotExist:
            pass

        # Check if s.a. number exists
        try:
            Employee.objects.get(sa_no=sa_no)
            errors.append('S.A. number is already taken.')
        except Employee.DoesNotExist:
            if not sa_no:
                errors.append('S.A. number must not be blank.')
            else:
                pass

        # Check if bday is blank
        if not date_of_birth:
            errors.append('Date of Birth must not be blank.')
        else:
            pass

        # Check if email exists   
        try:
            Employee.objects.get(email=email)
            errors.append('Email Address is already taken.')
        except Employee.DoesNotExist:
            if not email:
                errors.append('Email Address must not be blank.')
            else:
                pass

        if len(errors):
            error_message = {'errors': errors}
            raise serializers.ValidationError(error_message)

        return data

    def create(self, validated_data):
        username = validated_data['username']
        sa_no = validated_data['sa_no']
        email = validated_data['email']
        job_id = validated_data['job_id']
        supervisor = validated_data['supervisor']
        department_id = validated_data['department_id']
        department_role = validated_data['department_role']
        company_id = validated_data['company_id']
        date_employed = validated_data['date_employed']
        employee_status = validated_data['employee_status']
        salary = validated_data['salary']
        sick_leave_count = validated_data['sick_leave_count']
        vac_leave_count = validated_data['vac_leave_count']
        name = validated_data['name']
        nickname = validated_data['nickname']
        other_name = validated_data['other_name']
        employee_image = validated_data['employee_image']
        civil_status = validated_data['civil_status']
        citizenship = validated_data['citizenship']
        gender = validated_data['gender']
        weight = validated_data['weight']
        height = validated_data['height']
        date_of_birth = validated_data['date_of_birth']
        place_of_birth = validated_data['place_of_birth']
        city_address = validated_data['city_address']
        prov_address = validated_data['prov_address']
        tel_no = validated_data['tel_no']
        cel_no = validated_data['cel_no']
        religion = validated_data['religion']
        acr_no = validated_data['acr_no']
        acr_date = validated_data['acr_date']
        dept_labor_no = validated_data['dept_labor_no']
        dept_labor_date = validated_data['dept_labor_date']
        tin_no = validated_data['tin_no']
        sss_no = validated_data['sss_no']
        pagibig_no = validated_data['pagibig_no']
        philhealth_no = validated_data['philhealth_no']
        password = username + str(date_of_birth)

        new_employee = Employee(
            username=username,
            sa_no=sa_no,
            email=email,
            job_id=job_id,
            supervisor=supervisor,
            department_id=department_id,
            department_role=department_role,
            company_id=company_id,
            date_employed=date_employed,
            employee_status=employee_status,
            salary=salary,
            sick_leave_count=sick_leave_count,
            vac_leave_count=vac_leave_count,
            name = name,
            nickname = nickname,
            other_name = other_name,
            employee_image =  employee_image,
            civil_status = civil_status,
            citizenship = citizenship,
            gender = gender,
            weight = weight,
            height = height,
            date_of_birth = date_of_birth,
            place_of_birth = place_of_birth,
            city_address = city_address,
            prov_address = prov_address,
            tel_no = tel_no,
            cel_no = cel_no,
            religion = religion,
            acr_no = acr_no,
            acr_date = acr_date,
            dept_labor_no = dept_labor_no,
            dept_labor_date = dept_labor_date,
            tin_no = tin_no,
            sss_no = sss_no,
            pagibig_no = pagibig_no,
            philhealth_no = philhealth_no,
            password = password
        )

        new_employee.set_password(password)
        new_employee.save()

        return new_employee

class EmployeeHRLoginSerializer(serializers.ModelSerializer):

    employee_number = serializers.CharField(source='username', write_only=True)

    class Meta:
        model = Employee
        fields = ['employee_id', 'employee_number', 'password']
        extra_kwargs = {
            'employee_number': {'write_only': True},
            'password': {'write_only': True},
        }

    def validate(self, data):
        username = data['username']
        password = data['password']

        employee = authenticate(username=username, password=password)
        
        if employee:
            if employee.is_active:
                try:
                    if employee.department_role == 'HR':
                        data['employee'] = employee
                        return data
                    else:
                        raise serializers.ValidationError({'error': "Only HR is allowed to login."})
                except AttributeError:
                    raise serializers.ValidationError({'error': "User has no Department role yet."})
            else:
                raise serializers.ValidationError({'error': "Account is no longer valid."})
        else:
            raise serializers.ValidationError({'error': "Incorrect login credentials."})

class EmployeeLoginSerializer(serializers.ModelSerializer):

    employee_number = serializers.CharField(source='username', write_only=True)

    class Meta:
        model = Employee
        fields = ['employee_id', 'employee_number', 'password']
        extra_kwargs = {
            'employee_number': {'write_only': True},
            'password': {'write_only': True},
        }

    def validate(self, data):
        username = data['username']
        password = data['password']

        employee = authenticate(username=username, password=password)
        
        if employee:
            if employee.is_active:
                try:
                    data['employee'] = employee
                    return data
                except AttributeError:
                    raise serializers.ValidationError({'error': "User has no Department yet."})
            else:
                raise serializers.ValidationError({'errors': "Account is no longer valid."})
        else:
            raise serializers.ValidationError({'errors': "Incorrect login credentials."})

class IsAuthenticatedSerializer(serializers.Serializer):
    employee = serializers.UUIDField()

class EmployeeUpdateSerializer(serializers.ModelSerializer):

    job_id = serializers.SlugRelatedField(slug_field='job_id', queryset=Job.objects.all(), allow_null=True)
    supervisor = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=True)
    department_id = serializers.SlugRelatedField(slug_field='department_id', queryset=Department.objects.all(), allow_null=True)

    class Meta:
        model = Employee
        fields = ['employee_id', 'email', 'job_id', 'supervisor', 'department_id', 'department_role', 'company_id', 'date_employed', 'employee_status', 'salary', 
        'sick_leave_count', 'vac_leave_count', 'name', 'nickname', 'other_name', 'employee_image', 'civil_status', 'citizenship', 'gender', 
        'weight', 'height', 'date_of_birth','place_of_birth', 'city_address', 'prov_address', 'tel_no', 'cel_no', 'religion', 'acr_no', 'acr_date', 
        'dept_labor_no', 'dept_labor_date', 'tin_no', 'sss_no', 'pagibig_no', 'philhealth_no', 'is_active']
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.job_id = validated_data.get('job_id', instance.job_id)
        instance.supervisor = validated_data.get('supervisor', instance.supervisor)
        instance.department_id = validated_data.get('department_id', instance.department_id)
        instance.department_role = validated_data.get('department_role', instance.department_role)
        instance.company_id = validated_data.get('company_id', instance.company_id)
        instance.date_employed = validated_data.get('date_employed', instance.date_employed)
        instance.employee_status = validated_data.get('employee_status', instance.employee_status)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.sick_leave_count = validated_data.get('sick_leave_count', instance.sick_leave_count)
        instance.vac_leave_count = validated_data.get('vac_leave_count', instance.vac_leave_count)
        instance.name = validated_data.get('name', instance.name)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.other_name = validated_data.get('other_name', instance.other_name)
        instance.employee_image = validated_data.get('employee_image', instance.employee_image)
        instance.civil_status = validated_data.get('civil_status', instance.civil_status)
        instance.citizenship = validated_data.get('citizenship', instance.citizenship)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.height = validated_data.get('height', instance.height)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.place_of_birth = validated_data.get('place_of_birth', instance.place_of_birth)
        instance.city_address = validated_data.get('city_address', instance.city_address)
        instance.prov_address = validated_data.get('prov_address', instance.prov_address)
        instance.tel_no = validated_data.get('tel_no', instance.tel_no)
        instance.cel_no = validated_data.get('cel_no', instance.cel_no)
        instance.religion = validated_data.get('religion', instance.religion)
        instance.acr_no = validated_data.get('acr_no', instance.acr_no)
        instance.acr_date = validated_data.get('acr_date', instance.acr_date)
        instance.dept_labor_no = validated_data.get('dept_labor_no', instance.dept_labor_no)
        instance.dept_labor_date = validated_data.get('dept_labor_date', instance.dept_labor_date)
        instance.tin_no = validated_data.get('tin_no', instance.tin_no)
        instance.sss_no = validated_data.get('sss_no', instance.sss_no)
        instance.pagibig_no = validated_data.get('pagibig_no', instance.pagibig_no)
        instance.philhealth_no = validated_data.get('philhealth_no', instance.philhealth_no)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

class EmployeeViewSerializer(serializers.ModelSerializer):

    employee_number = serializers.CharField(source='username')
    
    class Meta:
        model = Employee
        fields = ['employee_id', 'employee_number', 'email', 'name', 'cel_no', 'department_id', 'department_role', 'company_id', 'employee_status']

class EmployeeRetrieveSerializer(serializers.ModelSerializer):

    job_id = serializers.SlugRelatedField(slug_field='job_id', read_only=True)
    supervisor = serializers.SlugRelatedField(slug_field='employee_id', read_only=True)
    department_id = serializers.SlugRelatedField(slug_field='department_id', read_only=True)
    employee_number = serializers.CharField(source='username')
    
    class Meta:
        model = Employee
        fields = ['employee_id', 'employee_number', 'sa_no', 'email', 'job_id', 'supervisor', 'department_id', 'department_role', 'company_id', 'date_employed', 
        'employee_status', 'salary', 'sick_leave_count', 'vac_leave_count', 'name', 'nickname', 'other_name', 'employee_image', 'civil_status', 'citizenship', 
        'gender', 'weight', 'height', 'date_of_birth', 'place_of_birth', 'city_address', 'prov_address', 'tel_no', 'cel_no', 'religion', 'acr_no', 'acr_date', 
        'dept_labor_no', 'dept_labor_date', 'tin_no', 'sss_no', 'pagibig_no', 'philhealth_no', 'is_active']

class ChangePasswordSerializer(serializers.ModelSerializer):

    old_password = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = Employee
        fields = ['old_password', 'password1', 'password2']

    def validate(self, data):
        old_password = data['old_password']
        password1 = data['password1']
        password2 = data['password2']

        employee = self.context['request'].user

        errors = []

        # Check if password matches
        if password1 != password2:
            errors.append('Password does not match.')

        # Check password requirements
        try:
            validate_password(password1)
        except:
            errors.append(
                'Passwords should be at least 8 characters consisted of characters, letters and numbers, and cannot be too common.')

        # Check if old_password matches current user's password
        if not employee.check_password(old_password):
            errors.append('Old password is incorrect.')

        # Check if new password matches current user's password
        if employee.check_password(password1):
            errors.append('You cannot use your old password as new password.')

        if len(errors):
            error_message = {'errors': errors}
            raise serializers.ValidationError(error_message)

        data['employee'] = employee
        return data

    def create(self, validated_data):
        password = validated_data['password1']
        employee = validated_data['employee']
        employee.set_password(password)
        employee.save()

        return employee

# Education
class EmployeeEducationSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeEducation
        fields = '__all__'

class EmployeeEducationCreateSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeEducation
        fields = '__all__'
    
    def validate(self, data):
        employee_id = data['employee_id']
        errors = []

        # Check if employee id exists
        try:
            EmployeeEducation.objects.get(employee_id=employee_id)
            errors.append('Employee Education Record already existed.')
        except EmployeeEducation.DoesNotExist:
            pass

        if len(errors):
            error_message = {'errors': errors}
            raise serializers.ValidationError(error_message)

        return data

class EmployeeEducationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeEducation
        fields = ['primary_school', 'primary_address', 'primary_grad', 'sec_school', 'sec_address', 'sec_grad',
        'col_school', 'col_address', 'col_degree', 'col_grad', 'grad_school', 'grad_address', 'grad_degree', 'grad_grad',
        'others']
        
# Job History
class EmployeeJobHistorySerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeJobHistory
        fields = '__all__'

# Exams Taken
class EmployeeExamsTakenSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeExamsTaken
        fields = '__all__'

# Seminars Taken
class EmployeeSeminarsTakenSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeSeminarsTaken
        fields = '__all__'

# Skills
class EmployeeSkillsSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeSkills
        fields = '__all__'

class EmployeeSkillsCreateSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeSkills
        fields = '__all__'
    
    def validate(self, data):
        employee_id = data['employee_id']
        errors = []

        # Check if employee id exists
        try:
            EmployeeSkills.objects.get(employee_id=employee_id)
            errors.append('Employee Skills Record already existed.')
        except EmployeeSkills.DoesNotExist:
            pass

        if len(errors):
            error_message = {'errors': errors}
            raise serializers.ValidationError(error_message)

        return data

class EmployeeSkillsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSkills
        fields = ['skill_name']

# Family Background
class EmployeeFamilySerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeFamily
        fields = '__all__'

class EmployeeFamilyCreateSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeFamily
        fields = '__all__'
    
    def validate(self, data):
        employee_id = data['employee_id']
        errors = []

        # Check if employee id exists
        try:
            EmployeeFamily.objects.get(employee_id=employee_id)
            errors.append('Employee Family Record already existed.')
        except EmployeeFamily.DoesNotExist:
            pass

        if len(errors):
            error_message = {'errors': errors}
            raise serializers.ValidationError(error_message)

        return data

class EmployeeFamilyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeFamily
        fields = ['father_name', 'father_birth', 'father_age', 'father_occu', 'father_employer',
        'mother_name', 'mother_birth', 'mother_age', 'mother_occu', 'mother_employer',
        'family_address', 'family_contact_no']

# Sibling
class EmployeeSiblingSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeSibling
        fields = '__all__'

# Married
class EmployeeMarriedSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeMarried
        fields = '__all__'

class EmployeeMarriedCreateSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeMarried
        fields = '__all__'
    
    def validate(self, data):
        employee_id = data['employee_id']
        errors = []

        # Check if employee id exists
        try:
            EmployeeMarried.objects.get(employee_id=employee_id)
            errors.append('Employee Married Record already existed.')
        except EmployeeMarried.DoesNotExist:
            pass

        if len(errors):
            error_message = {'errors': errors}
            raise serializers.ValidationError(error_message)

        return data

class EmployeeMarriedUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMarried
        fields = ['spouse_name', 'spouse_address', 'spouse_birth', 'spouse_age', 'spouse_occupation', 'spouse_employer']

# Children
class EmployeeChildrenSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeChildren
        fields = '__all__'

# Medical History
class EmployeeMedicalHistorySerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeMedicalHistory
        fields = '__all__'

class EmployeeMedicalHistoryCreateSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeMedicalHistory
        fields = '__all__'
    
    def validate(self, data):
        employee_id = data['employee_id']
        errors = []

        # Check if employee id exists
        try:
            EmployeeMedicalHistory.objects.get(employee_id=employee_id)
            errors.append('Medical History Record already existed.')
        except EmployeeMedicalHistory.DoesNotExist:
            pass

        if len(errors):
            error_message = {'errors': errors}
            raise serializers.ValidationError(error_message)

        return data
    
    def create(self, validated_data):
        employee_id = validated_data['employee_id']
        had_illness = validated_data['had_illness']
        illness_details = validated_data['illness_details']
        hospitalized = validated_data['hospitalized']
        hospitalized_details = validated_data['hospitalized_details']
        last_checkup_date = validated_data['last_checkup_date']
        last_checkup_purpose = validated_data['last_checkup_purpose']
        distinguishing_marks = validated_data['distinguishing_marks']

        return EmployeeMedicalHistory.objects.create(
            employee_id= employee_id,
            had_illness = had_illness,
            illness_details = illness_details,
            hospitalized = hospitalized,
            hospitalized_details = hospitalized_details,
            last_checkup_date = last_checkup_date,
            last_checkup_purpose = last_checkup_purpose,
            distinguishing_marks = distinguishing_marks
        )
    
class EmployeeMedicalHistoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMedicalHistory
        fields = ['had_illness', 'illness_details', 'hospitalized', 'hospitalized_details',  
        'last_checkup_purpose', 'last_checkup_place', 'last_checkup_date', 'distinguishing_marks']

class EmployeeMedicalHistoryViewSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeMedicalHistory
        fields = '__all__'

# Reference
class EmployeeReferenceSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeReference
        fields = '__all__'

# Organization
class EmployeeOrganizationSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeOrganization
        fields = '__all__'

# Offense
class EmployeeOffenseSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeOffense
        fields = '__all__'
        
class EmployeeOffenseCreateSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeOffense
        fields = '__all__'
    
    def validate(self, data):
        employee_id = data['employee_id']
        errors = []

        # Check if employee id exists
        try:
            EmployeeOffense.objects.get(employee_id=employee_id)
            errors.append('Record already existed.')
        except EmployeeOffense.DoesNotExist:
            pass

        if len(errors):
            error_message = {'errors': errors}
            raise serializers.ValidationError(error_message)

        return data
    
    def create(self, validated_data):
        employee_id = validated_data['employee_id']
        convicted = validated_data['convicted']
        offense_details = validated_data['offense_details']
        offense_court = validated_data['offense_court']
        date_filed = validated_data['date_filed']

        return EmployeeOffense.objects.create(
            employee_id= employee_id,
            convicted = convicted,
            offense_details = offense_details,
            offense_court = offense_court,
            date_filed = date_filed
        )
    
class EmployeeOffenseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeOffense
        fields = ['convicted', 'offense_details', 'offense_court', 'date_filed',
        'termination_record', 'revocation_record', 'injunction_record', 'arrest_record']

# In case of Emergency
class EmployeeEmergencySerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeEmergency
        fields = '__all__'
        
class EmployeeEmergencyCreateSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeEmergency
        fields = '__all__'
    
    def validate(self, data):
        employee_id = data['employee_id']
        errors = []

        # Check if employee id exists
        try:
            EmployeeEmergency.objects.get(employee_id=employee_id)
            errors.append('Record already existed.')
        except EmployeeEmergency.DoesNotExist:
            pass

        if len(errors):
            error_message = {'errors': errors}
            raise serializers.ValidationError(error_message)

        return data

class EmployeeEmergencyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeEmergency
        fields = ['person_name', 'person_relationship', 'person_address', 'person_phone']

# Signature
class EmployeeSignatureSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeSignature
        fields = '__all__'

# Documents
class EmployeeDocumentsSerializer(serializers.ModelSerializer):
    
    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = EmployeeDocuments
        fields = '__all__'