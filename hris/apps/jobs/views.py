from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import *

class JobViewset(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "job_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'retrieve': JobSerializer,
        'create': JobCreateSerializer, 
        'list': JobSerializer,
        'update': JobSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(JobViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return Job.objects.all()