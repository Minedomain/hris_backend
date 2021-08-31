from rest_framework import viewsets, generics, mixins, status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Announcement, Memo, PersonalMessage
from ..employees.models import Employee
from .serializers import *

class AnnouncementViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Announcement.objects.all().order_by('id')
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "announce_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': AnnouncementSerializer,
        'list': AnnouncementSerializer,
        'destroy': AnnouncementSerializer,
        'retrieve': AnnouncementSerializer,
    }

    def create(self, request):
        author_company = request.user.company_id
        author_department = request.user.department_id
        employee_id = request.user.employee_id

        try:
            if request.user.department_role == 'HR':
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()  

                hr = Employee.objects.get(employee_id=employee_id)
                employees_same_company = Employee.objects.filter(company_id=author_company).exclude(employee_id=employee_id).order_by('-id')

                messages = []
                for employee in employees_same_company:
                    message = PersonalMessage(message_sender=hr, message_receiver=employee, message_details='HR posted an announcement. Please check announcement page. Thank you.')
                    messages.append(message)
                
                PersonalMessage.objects.bulk_create(messages)

                return Response({
                    "message": "Announcement has been saved."
                }, status=status.HTTP_200_OK)

            elif request.user.department_role == 'Manager':
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()  

                manager = Employee.objects.get(employee_id=employee_id)
                employees_same_department = Employee.objects.filter(company_id=author_company).filter(Q(department_id=author_department) | Q(department_role='HR')).exclude(employee_id=employee_id).order_by('-id')

                messages = []
                for employee in employees_same_department:
                    message = PersonalMessage(message_sender=manager, message_receiver=employee, message_details='Department Manager posted an announcement. Please check announcement page. Thank you.')
                    messages.append(message)
                
                PersonalMessage.objects.bulk_create(messages)

                return Response({
                    "message": "Announcement has been saved."
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    "error": "Only the HR and Department Manager can post an announcement."
                }, status=status.HTTP_400_BAD_REQUEST)

        except (AttributeError, TypeError):
            return Response({
                    "error": "Something went wrong. Please try again."
                }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        company_id = request.user.company_id
        author_department = request.user.department_id
        filter_by_company = Announcement.objects.filter(announce_posted_by__company_id=company_id).filter(Q(announce_posted_by__department_id=author_department) | Q(announce_posted_by__department_role='HR')).order_by('-id')
        serializer = AnnouncementSerializer(filter_by_company, many=True)

        if serializer.data == []:
            return Response({'message': 'No Announcement yet.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
            
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': 'Announcement has been deleted successfully'}, status=status.HTTP_200_OK)

class AnnouncementRetrieveView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return Announcement.objects.filter(announce_posted_by__employee_id = employee_id).order_by('-id')
        except:
            return None
    
    def get(self, request):
        data = AnnouncementSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee announcement/s not found. Either the employee or announcement does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# Memo
class MemoViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Memo.objects.all().order_by('id')
    serializer_class = MemoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "memo_id"
    lookup_value_regex = "[^/]+"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': 'Memo has been deleted successfully'}, status=status.HTTP_200_OK)

class MemoSenderRetrieveView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return Memo.objects.filter(memo_posted_by__employee_id = employee_id).order_by('-id')
        except:
            return None
    
    def get(self, request):
        data = MemoSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee memo/s not found. Either the employee or memo does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

class MemoReceiverRetrieveView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            department_id = request.GET.get('department_id')
            if employee_id:
                filterRetrieve = Memo.objects.filter(memo_receiver_employee__employee_id = employee_id).order_by('-id')
            elif department_id:
                filterRetrieve = Memo.objects.filter(memo_receiver_dept__department_id = department_id).order_by('-id')
            return filterRetrieve
        except:
            return None
    
    def get(self, request):
        data = MemoSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Memo/s not found. Either the chosen employee/department or memo does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# Message
class PersonalMessageViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = PersonalMessage.objects.all().order_by('-id')
    serializer_class = PersonalMessageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "message_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': PersonalMessageCreateSerializer,
        'retrieve': PersonalMessageSerializer,
        'list': PersonalMessageSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(PersonalMessageViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return PersonalMessage.objects.all().order_by('-id')
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': 'Message has been deleted successfully'}, status=status.HTTP_200_OK)

class PersonalMessageListSpecificView(generics.ListAPIView):
    queryset = PersonalMessage.objects.all().order_by('-id')
    serializer_class = PersonalMessageSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        employee_id = request.user.employee_id

        try:
            filter_by_user = PersonalMessage.objects.filter(message_receiver__employee_id=employee_id).order_by('-id')
            serializer = PersonalMessageSerializer(filter_by_user, many=True)

            if serializer.data == []:
                return Response({'message': 'No message yet.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)

        except (AttributeError, TypeError):
            return Response({
                    "error": "Something went wrong. Please try again."
                }, status=status.HTTP_400_BAD_REQUEST)

class PersonalMessageSenderRetrieveView(generics.ListAPIView):
    serializer_class = PersonalMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return PersonalMessage.objects.filter(message_sender__employee_id = employee_id).order_by('-id')
        except:
            return None
    
    def get(self, request):
        data = PersonalMessageSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee message/s not found. Either the employee or message does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

class PersonalMessageReceiverRetrieveView(generics.ListAPIView):
    serializer_class = PersonalMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return PersonalMessage.objects.filter(message_receiver__employee_id = employee_id).order_by('-id')
        except:
            return None
    
    def get(self, request):
        data = PersonalMessageSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee message/s not found. Either the employee or message does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)