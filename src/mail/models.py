import uuid
from django.db import models

# Create your models here.
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_address = models.CharField("From", max_length=255)
    from_domain = models.CharField(max_length=64)
    to_address = models.CharField("To", max_length=255)
    to_domain = models.CharField(max_length=64)
    subject = models.CharField(max_length=255)
    client_ip = models.GenericIPAddressField("Client IP")
    mailscanner_hostname = models.CharField(max_length=255)
    spam_score = models.FloatField()
    timestamp = models.DateTimeField()
    token = models.CharField(max_length=255)
    whitelisted = models.BooleanField()
    blacklisted = models.BooleanField()
    is_spam = models.BooleanField()
    is_rbl_listed = models.BooleanField("Is RBL listed")
    quarantined = models.BooleanField()
    infected = models.BooleanField()

class RblReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id = models.ForeignKey('Message', on_delete=models.CASCADE)
    contents = models.TextField()

class SpamReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id = models.ForeignKey('Message', on_delete=models.CASCADE)
    contents = models.TextField()

class McpReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id = models.ForeignKey('Message', on_delete=models.CASCADE)
    contents = models.TextField()

class Headers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id = models.ForeignKey('Message', on_delete=models.CASCADE)
    contents = models.TextField()
