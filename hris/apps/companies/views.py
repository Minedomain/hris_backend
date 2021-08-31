from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializers import *

class CompanyViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('id')
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "company_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'retrieve': CompanySerializer,
        'create': CompanyCreateSerializer, 
        'list': CompanySerializer,
        'update': CompanySerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(CompanyViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return Company.objects.all()
