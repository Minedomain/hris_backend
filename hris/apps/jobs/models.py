import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Job(models.Model):
    job_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    job_title = models.CharField(max_length=255, blank=False)
    duties = models.CharField(max_length=255, blank=True, null=True, default=None)
    min_salary = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0.00)
    max_salary = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0.00)

    REQUIRED_FIELDS = []

    def __str__(self):
        return 'Job: ' + self.job_title
