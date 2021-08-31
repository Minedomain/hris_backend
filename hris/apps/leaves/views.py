from rest_framework import viewsets, generics, mixins, status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..engagements.models import PersonalMessage
from .models import Leave
from .serializers import *

class SmallPagesPagination(PageNumberPagination):  
    page_size = 10
    page_query_param = 'page'

class LeaveViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Leave.objects.all().order_by('id')
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "leave_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'retrieve': LeaveListSerializer,
        'create': LeaveSerializer, 
        'list': LeaveListSerializer,
        'update': LeaveUpdateSerializer
    }

    def create(self, request):
        author_status = request.user.employee_status
        author_supervisor = request.user.supervisor
        author_company = request.user.company_id
        employee_id = request.user.employee_id

        try:
            if author_status == 'Regular':
                # If no supervisor, leave request notification will be sent to HR
                if author_supervisor == None or author_supervisor == "":
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()   

                    sender = Employee.objects.get(employee_id=employee_id)
                    employee_hr = Employee.objects.filter(company_id=author_company).filter(department_role='HR').exclude(employee_id=employee_id).order_by('-id')

                    messages = []
                    for employee in employee_hr:
                        message = PersonalMessage(message_sender=sender, message_receiver=employee, message_details='An Employee has sent a Leave Request.')
                        messages.append(message)
                    
                    PersonalMessage.objects.bulk_create(messages)

                    return Response({
                        "message": "Leave request has been created."
                    }, status=status.HTTP_200_OK)

                # send leave request notification to supervisor
                else:
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()   

                    sender = Employee.objects.get(employee_id=employee_id)
                    employee_supervisor = Employee.objects.filter(employee_id=author_supervisor.employee_id).exclude(employee_id=employee_id).order_by('-id')

                    messages = []
                    for employee in employee_supervisor:
                        message = PersonalMessage(message_sender=sender, message_receiver=employee, message_details='An Employee has sent a Leave Request.')
                        messages.append(message)
                    
                    PersonalMessage.objects.bulk_create(messages)

                    return Response({
                        "message": "Leave request has been created."
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Only Regular Employees are allowed to file a leave request."
                }, status=status.HTTP_400_BAD_REQUEST)

        except (AttributeError, TypeError):
            return Response({
                    "error": "Something went wrong. Please try again."
                }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        department_name = request.user.department_id.department_name
        department_role = request.user.department_role
        author_company = request.user.company_id
        employee_id = request.user.employee_id
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        try:
            if department_role == 'HR':
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                leave_status = serializer.data['leave_status']
                employee_under_id = serializer.data['employee_id']
                
                if leave_status == 'Approved by HR':
                    sender = Employee.objects.get(employee_id=employee_id)
                    employee_under = Employee.objects.filter(employee_id=employee_under_id).exclude(employee_id=employee_id).order_by('-id')

                    messages = []
                    for employee in employee_under:
                        message = PersonalMessage(message_sender=sender, message_receiver=employee, message_details='HR has approved your leave request.')
                        messages.append(message)
                    
                    PersonalMessage.objects.bulk_create(messages)

                    return Response({'message':'Successfully updated leave status.', 'user':serializer.data})
                
                elif leave_status == 'Declined':
                    sender = Employee.objects.get(employee_id=employee_id)
                    employee_under = Employee.objects.filter(employee_id=employee_under_id).exclude(employee_id=employee_id).order_by('-id')

                    messages = []
                    for employee in employee_under:
                        message = PersonalMessage(message_sender=sender, message_receiver=employee, message_details='HR has declined your leave request.')
                        messages.append(message)
                    
                    PersonalMessage.objects.bulk_create(messages)

                    return Response({'message':'Successfully updated leave status.', 'user':serializer.data})

            elif department_role == 'Manager':
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                leave_status = serializer.data['leave_status']
                employee_under_id = serializer.data['employee_id']

                if leave_status == 'Approved by Supervisor':
                    sender = Employee.objects.get(employee_id=employee_id)
                    employee_under = Employee.objects.filter(employee_id=employee_under_id).exclude(employee_id=employee_id).order_by('-id')
                    employee_hr = Employee.objects.filter(company_id=author_company).filter(department_role="HR").exclude(employee_id=employee_id).order_by('-id')

                    messages = []
                    for employee in employee_under:
                        message = PersonalMessage(message_sender=sender, message_receiver=employee, message_details='Your Department Manager has approved your leave request. Please wait for the approval of HR.')
                        messages.append(message)

                    messages_hr = []
                    for hr in employee_hr:
                        message = PersonalMessage(message_sender=sender, message_receiver=hr, message_details=department_name + ' Manager has approved an Employee\'s leave request and is awaiting for your approval. Please check the leave request page to view.')
                        messages.append(message)
                    
                    PersonalMessage.objects.bulk_create(messages + messages_hr)

                    return Response({'message':'Successfully updated leave status.', 'user':serializer.data})

                elif leave_status == 'Declined':
                    sender = Employee.objects.get(employee_id=employee_id)
                    employee_under = Employee.objects.filter(employee_id=employee_under_id).exclude(employee_id=employee_id).order_by('-id')

                    messages = []
                    for employee in employee_under:
                        message = PersonalMessage(message_sender=sender, message_receiver=employee, message_details='Your Department Manager has declined your leave request.')
                        messages.append(message)
                    
                    PersonalMessage.objects.bulk_create(messages)

                    return Response({'message':'Successfully updated leave status.', 'user':serializer.data})
                    
            else:
                return Response({'message':'Only the HR and Manager can update leave status.'})
        
        except (AttributeError, TypeError, KeyError):
            return Response({'error': 'Something went wrong. Please try again.'})

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(LeaveViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return Leave.objects.all().order_by('-id')

class LeaveListSpecificView(generics.ListAPIView):
    queryset = Leave.objects.all().order_by('-id')
    serializer_class = LeaveListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallPagesPagination
    
    def list(self, request):
        employee_id = request.user.employee_id

        try:
            filter_by_user = Leave.objects.filter(employee_id__employee_id=employee_id).order_by('-id')
            serializer = LeaveListSerializer(filter_by_user, many=True)
            page = self.paginate_queryset(serializer.data)
            
            if serializer.data == []:
                return Response({'message': 'No filed leave yet.'}, status=status.HTTP_200_OK)
            else:
                return self.get_paginated_response(page)

        except (AttributeError, TypeError):
            return Response({
                    "error": "Something went wrong. Please try again."
                }, status=status.HTTP_400_BAD_REQUEST)


class LeaveListRequestsView(generics.ListAPIView):
    queryset = Leave.objects.all().order_by('-id')
    serializer_class = LeaveListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallPagesPagination

    def list(self, request, *args, **kwargs):
        employee_id = request.user.employee_id
        company_id = request.user.company_id
        department_id = request.user.department_id

        try:
            if request.user.department_role == 'HR':
                filter_request_hr = Leave.objects.filter(employee_id__company_id=company_id
                ).exclude(Q( (Q(Q(employee_id__supervisor__isnull = False) | Q(employee_id__supervisor = not None))) & Q(leave_status="Pending") )
                ).exclude(employee_id__employee_id=employee_id).order_by('-id')

                serializer = LeaveListSerializer(filter_request_hr, many=True)
                page = self.paginate_queryset(serializer.data)

                if serializer.data == []:
                    return Response({'message': 'No Leave Request yet.'}, status=status.HTTP_200_OK)
                else:
                    return self.get_paginated_response(page)
                    
            elif request.user.department_role == 'Manager':
                filter_request = Leave.objects.filter(employee_id__company_id=company_id
                ).filter(employee_id__department_id=department_id).filter(employee_id__supervisor__employee_id = employee_id
                ).exclude(employee_id__employee_id=employee_id).order_by('-id')
                serializer = LeaveListSerializer(filter_request, many=True)
                page = self.paginate_queryset(serializer.data)

                if serializer.data == []:
                    return Response({'message': 'No Leave Request yet.'}, status=status.HTTP_200_OK)
                else:
                    return self.get_paginated_response(page)
            else:
                return Response({'message': 'Only HR and Manager can receive Leave Requests.'}, status=status.HTTP_200_OK)

        except (AttributeError, TypeError):
            return Response({
                    "error": "Something went wrong. Please try again."
                }, status=status.HTTP_400_BAD_REQUEST)

class LeaveRetrieveView(generics.ListAPIView):
    serializer_class = LeaveListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return Leave.objects.filter(employee_id__employee_id = employee_id).order_by('-id')
        except:
            return None
    
    def get(self, request):
        data = LeaveListSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee leave request/s not found. Either the employee or leave request does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)