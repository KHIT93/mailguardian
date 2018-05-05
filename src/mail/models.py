import uuid
from django.db import models
from django.conf import settings
import os, datetime, subprocess, re

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
            return os.path.join(settings.MAILSCANNER_QUARANTINE_DIR, str(self.date).replace('-',''), "nonspam", self.mailq_id)
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

class SpamAssassinRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField(blank=True, null=True)

    def sync_files(self):
        # Sync spam assassin rule descriptions to database
        # grep -hr '^\s*describe' " . SA_RULES_DIR . ' /usr/share/spamassassin /usr/local/share/spamassassin ' . SA_PREFS . ' /etc/MailScanner/spam.assassin.prefs.conf /opt/MailScanner/etc/spam.assassin.prefs.conf /usr/local/etc/mail/spamassassin /etc/mail/spamassassin /var/lib/spamassassin 2>/dev/null | sort | uniq
        output = subprocess.check_output("/bin/grep -hr '^\s*describe' {0} {1} /etc/MailScanner/spam.assassin.prefs.conf /etc/mail/spamassassin /var/lib/spamassassin 2>/dev/null | /usr/bin/sort | /usr/bin/uniq".format(settings.SA_RULES_DIR, settings.SA_PREF), shell=True)
        descriptions = re.findall(r"^(?:\s*)describe\s+(\S+)\s+(.+)$", output.decode(), re.MULTILINE)
        for match in descriptions:
            rule, created = self.objects.get_or_create(key=match[0], value=match[1])
            if not created:
                rule.value = match[1]
                rule.save()
