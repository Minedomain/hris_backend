import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Department(models.Model):
    department_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    department_name = models.CharField(max_length=255, blank=False)
    department_details = models.CharField(max_length=255, blank=True, null=True, default=None)

    REQUIRED_FIELDS = []

    def __str__(self):
        return 'Department: ' + self.department_name
