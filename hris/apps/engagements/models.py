from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class Announcement(models.Model):
  announce_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
  announce_posted_by = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
  announce_subject = models.CharField(max_length=255, blank=False)
  announce_content = models.CharField(max_length=255, blank=False)
  announce_date = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
  
class Memo(models.Model):
  memo_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
  memo_subject = models.CharField(max_length=255, blank=False)
  memo_content = models.CharField(max_length=255, blank=False)
  memo_image = models.CharField(max_length=255, blank=True, null=True, default=None)
  memo_posted_by = models.ForeignKey('employees.Employee', related_name='memo_sender_employee', on_delete=models.CASCADE)
  memo_receiver_employee = models.ForeignKey('employees.Employee', related_name='memo_receiver_employee', on_delete=models.CASCADE, blank=True, null=True, default=None)
  memo_receiver_dept = models.ForeignKey('departments.Department', on_delete=models.CASCADE, blank=True, null=True, default=None)
  memo_date_created = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)

class PersonalMessage(models.Model):
  message_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
  message_sender = models.ForeignKey('employees.Employee', related_name='sender_employee', on_delete=models.CASCADE)
  message_receiver = models.ForeignKey('employees.Employee', related_name='receiver_employee', on_delete=models.CASCADE)
  message_details = models.CharField(max_length=255, blank=False)
  message_date_sent = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
  message_is_read = models.BooleanField(default=False)
