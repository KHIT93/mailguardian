import uuid
from django.db import models
from auditlog.registry import auditlog
from django.conf import settings

# https://gist.github.com/solusipse/7ed8e1da104baaee3f05

# Create your models here.

# This maps to postfix virtual_mailbox_domains and virtual_transport
class Domain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    destination = models.CharField(max_length=128, null=True, blank=True)
    relay_type = models.CharField(max_length=64, default='smtp')
    created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_timestamp = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    catchall = models.BooleanField(default=False)
    # For commercial use in order to limit the number of recipient mailboxes that can be created
    allowed_accounts = models.IntegerField(default=-1)

    def __str__(self):
        return self.name

# class Forwarder(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     source = models.CharField(max_length=80, unique=True)
#     destination = models.TextField()

# class Transport(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     domain = models.CharField(max_length=128, unique=True)
#     transport = models.CharField(max_length=128)

if settings.AUDIT_LOGGING:
    auditlog.register(Domain)