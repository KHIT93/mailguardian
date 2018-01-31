import uuid
from django.db import models

# https://gist.github.com/solusipse/7ed8e1da104baaee3f05

# Create your models here.

# This maps to postfix virtual_mailbox_domains and virtual_transport
class Domain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain = models.CharField(max_length=128, unique=True)
    destination = models.CharField(max_length=128)
    relay_destination = models.CharField(max_length=128)
    relay_type = models.CharField(max_length=64, default='smtp')
    created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_timestamp = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    # For commercial use in order to limit the number of recipient mailboxes that can be created
    allowed_accounts = models.IntegerField(default=-1)
    
    def save(self, *args, **kwargs):
        self.relay_destination = self.relay_type + ':[' + self.destination + ']'
        super(Domain, self).save(*args, **kwargs)

# class Forwarder(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     source = models.CharField(max_length=80, unique=True)
#     destination = models.TextField()

# class MailUser(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     email = models.CharField(max_length=80, unique=True)

# class Transport(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     domain = models.CharField(max_length=128, unique=True)
#     transport = models.CharField(max_length=128)