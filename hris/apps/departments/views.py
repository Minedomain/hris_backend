from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Department
from .serializers import *

class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('id')
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "department_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'retrieve': DepartmentSerializer,
        'create': DepartmentCreateSerializer, 
        'list': DepartmentSerializer,
        'update': DepartmentSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(DepartmentViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return Department.objects.all()