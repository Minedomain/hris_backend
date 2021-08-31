from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class Attendance(models.Model):
  attendance_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
  employee_id = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
  datetime_in = models.DateTimeField(max_length=255, blank=True, null=True, default=None)
  datetime_out = models.DateTimeField(max_length=255, blank=True, null=True, default=None)
  hours_logged = models.IntegerField(default=0)
  absent = models.BooleanField(default=False)