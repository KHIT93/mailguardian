import uuid
from django.db import models
from django.conf import settings
import os, datetime

# Create your models here.
class Message(models.Model):
    class Meta:
        ordering = ('-timestamp',)
        get_latest_by = 'timestamp'
        indexes = [
            models.Index(fields=['from_address', 'from_domain']),

            models.Index(fields=['to_address', 'to_domain']),

            models.Index(fields=['from_address', 'to_address']),

            models.Index(fields=['from_address', 'to_domain']),

            models.Index(fields=['to_address', 'from_domain']),

            models.Index(fields=['client_ip', 'mailscanner_hostname']),

            models.Index(fields=['from_address', 'blacklisted']),
            models.Index(fields=['from_address', 'whitelisted']),
            models.Index(fields=['from_address', 'infected']),
            models.Index(fields=['from_address', 'is_spam']),
            models.Index(fields=['from_address', 'quarantined']),
            models.Index(fields=['from_address', 'is_rbl_listed']),

            models.Index(fields=['to_address', 'blacklisted']),
            models.Index(fields=['to_address', 'whitelisted']),
            models.Index(fields=['to_address', 'infected']),
            models.Index(fields=['to_address', 'is_spam']),
            models.Index(fields=['to_address', 'quarantined']),
            models.Index(fields=['to_address', 'is_rbl_listed']),

            models.Index(fields=['from_domain', 'blacklisted']),
            models.Index(fields=['from_domain', 'whitelisted']),
            models.Index(fields=['from_domain', 'infected']),
            models.Index(fields=['from_domain', 'is_spam']),
            models.Index(fields=['from_domain', 'quarantined']),
            models.Index(fields=['from_domain', 'is_rbl_listed']),

            models.Index(fields=['to_domain', 'blacklisted']),
            models.Index(fields=['to_domain', 'whitelisted']),
            models.Index(fields=['to_domain', 'infected']),
            models.Index(fields=['to_domain', 'is_spam']),
            models.Index(fields=['to_domain', 'quarantined']),
            models.Index(fields=['to_domain', 'is_rbl_listed']),

            models.Index(fields=['client_ip', 'blacklisted']),
            models.Index(fields=['client_ip', 'whitelisted']),
            models.Index(fields=['client_ip', 'infected']),
            models.Index(fields=['client_ip', 'is_spam']),
            models.Index(fields=['client_ip', 'quarantined']),
            models.Index(fields=['client_ip', 'is_rbl_listed']),

            models.Index(fields=['mailscanner_hostname', 'blacklisted']),
            models.Index(fields=['mailscanner_hostname', 'whitelisted']),
            models.Index(fields=['mailscanner_hostname', 'infected']),
            models.Index(fields=['mailscanner_hostname', 'is_spam']),
            models.Index(fields=['mailscanner_hostname', 'quarantined']),
            models.Index(fields=['mailscanner_hostname', 'is_rbl_listed']),
        ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_address = models.CharField("From", max_length=511, blank=True, default="", db_index=True)
    from_domain = models.CharField(max_length=255, blank=True, default="", db_index=True)
    to_address = models.CharField("To", max_length=511, blank=True, default="", db_index=True)
    to_domain = models.CharField(max_length=255, blank=True, default="", db_index=True)
    subject = models.TextField(blank=True, default="", db_index=True)
    client_ip = models.GenericIPAddressField("Client IP", db_index=True, null=True)
    mailscanner_hostname = models.CharField(max_length=255, db_index=True)
    spam_score = models.DecimalField(db_index=True, default=0.00, max_digits=7, decimal_places=2)
    mcp_score = models.DecimalField(db_index=True, default=0.00, max_digits=7, decimal_places=2, blank=True, null=True)
    timestamp = models.DateTimeField(db_index=True)
    date = models.DateField(db_index=True)
    size = models.FloatField(default=0)
    token = models.CharField(max_length=255, null=True)
    mailq_id = models.TextField("Mailqueue identification", null=True)
    whitelisted = models.BooleanField(db_index=True, default=False)
    blacklisted = models.BooleanField(db_index=True, default=False)
    is_spam = models.BooleanField(db_index=True, default=False)
    is_mcp = models.BooleanField(db_index=True, default=False)
    is_rbl_listed = models.BooleanField("Is RBL listed", db_index=True, default=False)
    quarantined = models.BooleanField(db_index=True, default=False)
    infected = models.BooleanField(db_index=True, default=False)
    released = models.BooleanField(db_index=True, default=False)

    def __str__(self):
        return str(self.id) + "[" + str(self.from_address) + " to " + str(self.to_address) + "]"

    def file_path(self):
        if self.mailq_id:
            return os.path.join(settings.MAILSCANNER_QUARANTINE_DIR, str(datetime.date.today()).replace('-',''), "nonspam", self.mailq_id)
        else:
            return None
    
    def queue_file_exists(self):
        if self.file_path():
            if os.path.isfile(self.file_path()):
                return True
        return False

class RblReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.OneToOneField('Message', on_delete=models.CASCADE, unique=True)
    contents = models.TextField(null=True, blank=True)

class SpamReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.OneToOneField('Message', on_delete=models.CASCADE, unique=True)
    contents = models.TextField(null=True, blank=True)

class McpReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.OneToOneField('Message', on_delete=models.CASCADE, unique=True)
    contents = models.TextField(null=True, blank=True)

class MailscannerReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.OneToOneField('Message', on_delete=models.CASCADE, unique=True)
    contents = models.TextField(null=True, blank=True)

class Headers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.OneToOneField('Message', on_delete=models.CASCADE, unique=True)
    contents = models.TextField(null=True, blank=True)
