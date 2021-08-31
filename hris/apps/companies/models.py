import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Company(models.Model):
    company_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
    company_name = models.CharField(max_length=255, blank=False)
    company_description = models.CharField(max_length=255, blank=True, null=True, default=None)
    company_address = models.CharField(max_length=255, blank=True, null=True, default=None)

    REQUIRED_FIELDS = []

    def __str__(self):
        return 'Company: ' + self.company_name