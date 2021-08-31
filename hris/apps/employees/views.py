from rest_framework import viewsets, generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..permissions import IsHRDepartment
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage
from django.template.loader import get_template
from .models import *
from .serializers import *

class EmployeeRegisterView(generics.GenericAPIView):
    serializer_class = EmployeeRegisterSerializer
    permission_classes = [IsHRDepartment]

    def post(self, request):
        """
        Registration of Employee.
        """
        serializer = EmployeeRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        employee = serializer.save()
        serialized_employee_data = EmployeeRegisterSerializer(employee).data
        '''
        if employee.company_id:
            employee_company = employee.company_id.company_name
        else:
            employee_company = None

        employee_number = employee.username
        employee_email = employee.email
        employee_birth_date = employee.date_of_birth
        html_template = get_template('send/welcome.html')
        title = 'Welcome'

        context = {
            "action": "Welcome to the company",
            "employee_number": employee_number,
            "company": employee_company,
            "email": employee_email,
            "birth_date": employee_birth_date,
        }

        html_content = html_template.render(context)

        email = EmailMessage(
            subject=title,
            body=html_content,
            from_email="HR",
            to=[employee_email],
        )
        email.content_subtype = "html"
        email.send()
        '''
        return Response({'user': serialized_employee_data}, status=status.HTTP_201_CREATED)

class EmployeeLoginView(generics.GenericAPIView):
    serializer_class = EmployeeLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Employee Login.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        employee = serializer.validated_data['employee']
        token = Token.objects.get_or_create(user=employee)

        token = token[0].key
        
        serialized_employee_data = EmployeeLoginSerializer(employee).data

        return Response({'token': token, 'user':serialized_employee_data}, status=status.HTTP_200_OK)

class EmployeeHRLoginView(generics.GenericAPIView):
    serializer_class = EmployeeHRLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Employee Login.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        employee = serializer.validated_data['employee']
        token = Token.objects.get_or_create(user=employee)

        token = token[0].key
        
        serialized_employee_data = EmployeeLoginSerializer(employee).data

        return Response({'token': token, 'user':serialized_employee_data}, status=status.HTTP_200_OK)

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Change password of user.
        """
        serializer = self.serializer_class(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({
            "message": "Password has been successfully changed."
        }, status=status.HTTP_202_ACCEPTED)

class IsAuthenticatedView(generics.GenericAPIView):
    serializer_class = IsAuthenticatedSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Check if user is still logged in or has an existing auth token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        employee_uuid = serializer.validated_data['employee']

        try:
            employee = Employee.objects.get(employee_id=employee_uuid)

            try:
                Token.objects.get(user=employee)
                return Response({'is_authenticated': True}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'is_authenticated': False}, status=status.HTTP_200_OK)

        except Employee.DoesNotExist:
            return Response({'error': 'Employee does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

class EmployeeLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            return Response({"message": "User is already logged out."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User has been successfully logged out."}, status=status.HTTP_200_OK)

class EmployeeViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Employee.objects.all().order_by('id')
    serializer_class = EmployeeViewSerializer
    permission_classes = [AllowAny]
    lookup_field = "employee_id"
    lookup_value_regex = "[^/]+"
    
    action_serializers = {
        'update': EmployeeUpdateSerializer,
        'partial_update': EmployeeUpdateSerializer,
        'retrieve': EmployeeRetrieveSerializer,
        'list': EmployeeViewSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(EmployeeViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return Employee.objects.all()

# Education
class EmployeeEducationViewset(viewsets.ModelViewSet):
    queryset = EmployeeEducation.objects.all().order_by('id')
    serializer_class = EmployeeEducationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "employee_id__employee_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': EmployeeEducationCreateSerializer, 
        'retrieve': EmployeeEducationSerializer,
        'list': EmployeeEducationSerializer,
        'update': EmployeeEducationUpdateSerializer
    }
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(EmployeeEducationViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return EmployeeEducation.objects.all()

# Job History
class EmployeeJobHistoryViewset(viewsets.ModelViewSet):
    queryset = EmployeeJobHistory.objects.all().order_by('id')
    serializer_class = EmployeeJobHistorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "job_history_id"
    lookup_value_regex = "[^/]+"

class EmployeeJobHistoryRetrieveView(generics.ListAPIView):
    serializer_class = EmployeeJobHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return EmployeeJobHistory.objects.filter(employee_id__employee_id = employee_id)
        except:
            return None
    
    def get(self, request):
        data = EmployeeJobHistorySerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee job history not found. Either the employee or job history does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# Exams Taken
class EmployeeExamsTakenViewset(viewsets.ModelViewSet):
    queryset = EmployeeExamsTaken.objects.all().order_by('id')
    serializer_class = EmployeeExamsTakenSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "exam_id"
    lookup_value_regex = "[^/]+"

class EmployeeExamsTakenRetrieveView(generics.ListAPIView):
    serializer_class = EmployeeExamsTakenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return EmployeeExamsTaken.objects.filter(employee_id__employee_id = employee_id)
        except:
            return None
    
    def get(self, request):
        data = EmployeeExamsTakenSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee exam/s taken not found. Either the employee or exam taken does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# Seminars Taken
class EmployeeSeminarsTakenViewset(viewsets.ModelViewSet):
    queryset = EmployeeSeminarsTaken.objects.all().order_by('id')
    serializer_class = EmployeeSeminarsTakenSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "seminar_id"
    lookup_value_regex = "[^/]+"

class EmployeeSeminarsTakenRetrieveView(generics.ListAPIView):
    serializer_class = EmployeeSeminarsTakenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return EmployeeSeminarsTaken.objects.filter(employee_id__employee_id = employee_id)
        except:
            return None
    
    def get(self, request):
        data = EmployeeSeminarsTakenSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee seminar/s taken not found. Either the employee or seminar taken does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# Skills
class EmployeeSkillsViewset(viewsets.ModelViewSet):
    queryset = EmployeeSkills.objects.all().order_by('id')
    serializer_class = EmployeeSkillsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "employee_id__employee_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': EmployeeSkillsCreateSerializer, 
        'retrieve': EmployeeSkillsSerializer,
        'list': EmployeeSkillsSerializer,
        'update': EmployeeSkillsUpdateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(EmployeeSkillsViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return EmployeeSkills.objects.all()

# Family Background
class EmployeeFamilyViewset(viewsets.ModelViewSet):
    queryset = EmployeeFamily.objects.all().order_by('id')
    serializer_class = EmployeeFamilySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "employee_id__employee_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': EmployeeFamilyCreateSerializer, 
        'retrieve': EmployeeFamilySerializer,
        'list': EmployeeFamilySerializer,
        'update': EmployeeFamilyUpdateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(EmployeeFamilyViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return EmployeeFamily.objects.all()

# Sibling
class EmployeeSiblingViewset(viewsets.ModelViewSet):
    queryset = EmployeeSibling.objects.all().order_by('id')
    serializer_class = EmployeeSiblingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "sibling_id"
    lookup_value_regex = "[^/]+"

class EmployeeSiblingRetrieveView(generics.ListAPIView):
    serializer_class = EmployeeSiblingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return EmployeeSibling.objects.filter(employee_id__employee_id = employee_id)
        except:
            return None
    
    def get(self, request):
        data = EmployeeSiblingSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee sibling/s not found. Either the employee or sibling does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# If Married
class EmployeeMarriedViewset(viewsets.ModelViewSet):
    queryset = EmployeeMarried.objects.all().order_by('id')
    serializer_class = EmployeeMarriedSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "employee_id__employee_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': EmployeeMarriedCreateSerializer, 
        'retrieve': EmployeeMarriedSerializer,
        'list': EmployeeMarriedSerializer,
        'update': EmployeeMarriedUpdateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(EmployeeMarriedViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return EmployeeMarried.objects.all()

# Children
class EmployeeChildrenViewset(viewsets.ModelViewSet):
    queryset = EmployeeChildren.objects.all().order_by('id')
    serializer_class = EmployeeChildrenSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "child_id"
    lookup_value_regex = "[^/]+"

class EmployeeChildrenRetrieveView(generics.ListAPIView):
    serializer_class = EmployeeChildrenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return EmployeeChildren.objects.filter(employee_id__employee_id = employee_id)
        except:
            return None
    
    def get(self, request):
        data = EmployeeChildrenSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee children not found. Either the employee or children does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# Medical History
class EmployeeMedicalHistoryViewset(viewsets.ModelViewSet):
    queryset = EmployeeMedicalHistory.objects.all().order_by('id')
    serializer_class = EmployeeMedicalHistorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "employee_id__employee_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': EmployeeMedicalHistoryCreateSerializer, 
        'retrieve': EmployeeMedicalHistoryViewSerializer,
        'list': EmployeeMedicalHistoryViewSerializer,
        'update': EmployeeMedicalHistoryUpdateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(EmployeeMedicalHistoryViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return EmployeeMedicalHistory.objects.all()

# Reference
class EmployeeReferenceViewset(viewsets.ModelViewSet):
    queryset = EmployeeReference.objects.all().order_by('id')
    serializer_class = EmployeeReferenceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "ref_id"
    lookup_value_regex = "[^/]+"

class EmployeeReferenceRetrieveView(generics.ListAPIView):
    serializer_class = EmployeeReferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return EmployeeReference.objects.filter(employee_id__employee_id = employee_id)
        except:
            return None
    
    def get(self, request):
        data = EmployeeReferenceSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee reference/s not found. Either the employee or reference does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# Organization
class EmployeeOrganizationViewset(viewsets.ModelViewSet):
    queryset = EmployeeOrganization.objects.all().order_by('id')
    serializer_class = EmployeeOrganizationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "org_id"
    lookup_value_regex = "[^/]+"

class EmployeeOrganizationRetrieveView(generics.ListAPIView):
    serializer_class = EmployeeOrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return EmployeeOrganization.objects.filter(employee_id__employee_id = employee_id)
        except:
            return None
    
    def get(self, request):
        data = EmployeeOrganizationSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee organization/s not found. Either the employee or organization does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# Offense
class EmployeeOffenseViewset(viewsets.ModelViewSet):
    queryset = EmployeeOffense.objects.all().order_by('id')
    serializer_class = EmployeeOffenseCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "employee_id__employee_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': EmployeeOffenseCreateSerializer, 
        'retrieve': EmployeeOffenseSerializer,
        'list': EmployeeOffenseSerializer,
        'update': EmployeeOffenseUpdateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(EmployeeOffenseViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return EmployeeOffense.objects.all()

# In Case of Emergency
class EmployeeEmergencyViewset(viewsets.ModelViewSet):
    queryset = EmployeeEmergency.objects.all().order_by('id')
    serializer_class = EmployeeEmergencyCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "employee_id__employee_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': EmployeeEmergencyCreateSerializer, 
        'retrieve': EmployeeEmergencySerializer,
        'list': EmployeeEmergencySerializer,
        'update': EmployeeEmergencyUpdateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(EmployeeEmergencyViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return EmployeeEmergency.objects.all()

# Signature
class EmployeeSignatureViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = EmployeeSignature.objects.all().order_by('id')
    serializer_class = EmployeeSignatureSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "employee_id__employee_id"
    lookup_value_regex = "[^/]+"

# Documents
class EmployeeDocumentsViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,viewsets.GenericViewSet):
    queryset = EmployeeOffense.objects.all().order_by('id')
    serializer_class = EmployeeDocumentsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "docu_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': EmployeeDocumentsSerializer,
        'retrieve': EmployeeDocumentsSerializer,
        'list': EmployeeDocumentsSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(EmployeeDocumentsViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return EmployeeDocuments.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': 'Document has been deleted successfully'},status=status.HTTP_200_OK)

class EmployeeDocumentsRetrieveView(generics.ListAPIView):
    serializer_class = EmployeeDocumentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return EmployeeDocuments.objects.filter(employee_id__employee_id = employee_id)
        except:
            return None
    
    def get(self, request):
        data = EmployeeDocumentsSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee document/s not found. Either the employee or document does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)