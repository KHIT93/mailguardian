import uuid
from django.db import models
from django.conf import settings
import os, datetime, subprocess
from django.utils.translation import gettext_lazy as _

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
            models.Index(fields=['from_address', 'blocked']),
            models.Index(fields=['from_address', 'allowed']),
            models.Index(fields=['from_address', 'infected']),
            models.Index(fields=['from_address', 'is_spam']),
            models.Index(fields=['from_address', 'stored']),
            models.Index(fields=['from_address', 'is_rbl_listed']),
            models.Index(fields=['to_address', 'blocked']),
            models.Index(fields=['to_address', 'allowed']),
            models.Index(fields=['to_address', 'infected']),
            models.Index(fields=['to_address', 'is_spam']),
            models.Index(fields=['to_address', 'stored']),
            models.Index(fields=['to_address', 'is_rbl_listed']),
            models.Index(fields=['from_domain', 'blocked']),
            models.Index(fields=['from_domain', 'allowed']),
            models.Index(fields=['from_domain', 'infected']),
            models.Index(fields=['from_domain', 'is_spam']),
            models.Index(fields=['from_domain', 'stored']),
            models.Index(fields=['from_domain', 'is_rbl_listed']),
            models.Index(fields=['to_domain', 'blocked']),
            models.Index(fields=['to_domain', 'allowed']),
            models.Index(fields=['to_domain', 'infected']),
            models.Index(fields=['to_domain', 'is_spam']),
            models.Index(fields=['to_domain', 'stored']),
            models.Index(fields=['to_domain', 'is_rbl_listed']),
            models.Index(fields=['client_ip', 'blocked']),
            models.Index(fields=['client_ip', 'allowed']),
            models.Index(fields=['client_ip', 'infected']),
            models.Index(fields=['client_ip', 'is_spam']),
            models.Index(fields=['client_ip', 'stored']),
            models.Index(fields=['client_ip', 'is_rbl_listed']),
            models.Index(fields=['mailscanner_hostname', 'blocked']),
            models.Index(fields=['mailscanner_hostname', 'allowed']),
            models.Index(fields=['mailscanner_hostname', 'infected']),
            models.Index(fields=['mailscanner_hostname', 'is_spam']),
            models.Index(fields=['mailscanner_hostname', 'stored']),
            models.Index(fields=['mailscanner_hostname', 'is_rbl_listed']),
        ]
        verbose_name = _('message')
        verbose_name_plural = _('messages')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_address = models.TextField(_("From"), blank=True, default="", db_index=True)
    from_domain = models.TextField(blank=True, default="", db_index=True)
    to_address = models.TextField(_("To"), blank=True, default="", db_index=True)
    to_domain = models.TextField(_('To domain'), blank=True, default="", db_index=True)
    subject = models.TextField(_('Subject'), blank=True, default="", db_index=True)
    client_ip = models.GenericIPAddressField(_("Client IP"), db_index=True, null=True)
    mailscanner_hostname = models.CharField(_('MailScanner Host'), max_length=255, db_index=True)
    spam_score = models.DecimalField(_('Spam Score'), db_index=True, default=0.00, max_digits=7, decimal_places=2)
    mcp_score = models.DecimalField(_('MCP Score'), db_index=True, default=0.00, max_digits=7, decimal_places=2, blank=True, null=True)
    timestamp = models.DateTimeField(_('Timestamp'), db_index=True)
    date = models.DateField(_('Date'), db_index=True)
    size = models.FloatField(_('Size'), default=0)
    token = models.CharField(_('Token'), max_length=255, null=True)
    mailq_id = models.TextField(_("Mailqueue identification"), null=True)
    allowed = models.BooleanField(_('Allowed'), db_index=True, default=False)
    blocked = models.BooleanField(_('Blocked'), db_index=True, default=False)
    is_spam = models.BooleanField(_('Is Spam'), db_index=True, default=False)
    is_mcp = models.BooleanField(_('Is MCP'), db_index=True, default=False)
    is_rbl_listed = models.BooleanField(_("Listed in RBL"), db_index=True, default=False)
    stored = models.BooleanField(_('Stored'), db_index=True, default=False)
    scanned = models.BooleanField(_('Message has been scanned'),db_index=True, default=True)
    infected = models.BooleanField(_('Infected'), db_index=True, default=False)
    released = models.BooleanField(_('Released'), db_index=True, default=False)

    def __str__(self):
        return str(self.id) + "[" + str(self.from_address) + " to " + str(self.to_address) + "]"

    def file_path(self):
        if self.mailq_id:
            folder = "nonspam" if not self.is_spam else "spam"
            return os.path.join(settings.MAILSCANNER_QUARANTINE_DIR, str(self.date).replace('-',''), folder, self.mailq_id)
        else:
            return None
    
    def queue_file_exists(self):
        if self.file_path():
            if os.path.isfile(self.file_path()):
                return True
        return False

class RblReport(models.Model):
    class Meta:
        verbose_name = _('RBL report')
        verbose_name_plural = _('RBL reports')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.OneToOneField('Message', on_delete=models.CASCADE, unique=True)
    contents = models.TextField(null=True, blank=True)

class SpamReport(models.Model):
    class Meta:
        verbose_name = _('spam report')
        verbose_name_plural = _('spam reports')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.OneToOneField('Message', on_delete=models.CASCADE, unique=True)
    contents = models.TextField(null=True, blank=True)

class McpReport(models.Model):
    class Meta:
        verbose_name = _('MCP report')
        verbose_name_plural = _('MCP reports')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.OneToOneField('Message', on_delete=models.CASCADE, unique=True)
    contents = models.TextField(null=True, blank=True)

class MailscannerReport(models.Model):
    class Meta:
        verbose_name = _('mailscanner report')
        verbose_name_plural = _('mailscanner reports')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.OneToOneField('Message', on_delete=models.CASCADE, unique=True)
    contents = models.TextField(null=True, blank=True)

class Headers(models.Model):
    class Meta:
        verbose_name = _('headers')
        verbose_name_plural = _('headers')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.OneToOneField('Message', on_delete=models.CASCADE, unique=True)
    contents = models.TextField(null=True, blank=True)

class TransportLog(models.Model):
    class Meta:
        ordering = ('timestamp',)
        get_latest_by = 'timestamp'
        verbose_name = _('transport log entry')
        verbose_name_plural = _('transport log entries')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(_('Timestamp'), db_index=True)
    transport_host = models.CharField(_('Transported by'), max_length=255, db_index=True)
    transport_type = models.CharField(_('Transportation Type'), max_length=255, db_index=True)
    relay_host = models.CharField(_('Relayed to'), max_length=255, db_index=True)
    dsn = models.CharField(('DSN'), max_length=255, db_index=True)
    dsn_message = models.TextField(_('DSN Message'), db_index=True)
    delay = models.DurationField(_('Delay'))

class SmtpRelay(models.Model):
    class Meta:
        verbose_name = _('smtp relay')
        verbose_name_plural = _('smtp relays')
        ordering = ('ip_address', 'hostname')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.CharField(_("IP Address"), max_length=255, db_index=True)
    hostname = models.CharField(_('Hostname'), max_length=255, db_index=True, default='')
    active = models.BooleanField(_('Active'), default=0)
    comment = models.TextField(_('Comment'))
