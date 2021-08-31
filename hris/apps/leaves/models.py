from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class Leave(models.Model):
  PENDING = 'Pending'
  APPROVED_SUPERVISOR = 'Approved by Supervisor'
  APPROVED_HR = 'Approved by HR'
  DECLINED = 'Declined'
  STATUS = [
      (PENDING , _('Pending')),
      (APPROVED_SUPERVISOR, _('Approved by Supervisor')),
      (APPROVED_HR, _('Approved by HR')),
      (DECLINED, _('Declined')),
  ]
  leave_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
  employee_id = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
  leave_type = models.CharField(max_length=255, blank=False)
  leave_reason = models.CharField(max_length=255, blank=False)
  date_filed = models.DateField(max_length=255, blank=False)
  leave_status = models.CharField(max_length=255, choices=STATUS, default=PENDING)