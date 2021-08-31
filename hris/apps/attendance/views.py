from rest_framework import viewsets, generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Attendance
from .serializers import *

class AttendanceViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Attendance.objects.all().order_by('id')
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "attendance_id"
    lookup_value_regex = "[^/]+"

class AttendanceRetrieveView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            employee_id = request.GET.get('employee_id')
            return Attendance.objects.filter(employee_id__employee_id = employee_id)
        except:
            return None
    
    def get(self, request):
        data = AttendanceSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Employee attendance not found. Either the employee or attendance does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)