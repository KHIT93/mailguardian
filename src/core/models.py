from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import uuid
from os import listdir
from os.path import isfile, join
import importlib
#from django.contrib.auth.models import AbstractUser

# Create your models here.
class MailScannerConfiguration(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['key']),
        ]
        unique_together = ('key', 'value')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255)
    value = models.TextField()
    filepath = models.CharField(max_length=511, default=settings.MAILSCANNER_CONFIG_DIR + '/MailScanner.conf')

    def __str__(self):
        return str(self.key)

    @staticmethod
    def sync_files_to_db():
        files = [f for f in listdir(settings.MAILSCANNER_CONFIG_DIR) if isfile(join(settings.MAILSCANNER_CONFIG_DIR, f))]
        for f in files:
            parser = None
            classname = f.replace('.', ' ').title().replace(' ', '') + 'FileParser'
            try:
                module = importlib.import_module('core.fileparsers')
                classname = getattr(module, classname)
                parser = classname()
            except AttributeError:
                parser = None
            if parser:
                parser.parse(f)
            else:
                print('Parser {0} does not exist'.format(classname))

    
    @staticmethod
    def rebuild_config_files(self, file):
        return None

    def update_config_parameter(self):
        return None

class SpamAssassinConfiguration(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['key']),
        ]
        unique_together = ('key', 'value')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255)
    rule = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    filepath = models.CharField(max_length=511, default=settings.MAILSCANNER_CONFIG_DIR + '/spamassassin.conf')

class Setting(models.Model):
    class Meta:
        db_table = 'core_settings'
        ordering = ('key',)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.key)

class AuditLog(models.Model):
    class Meta:
        ordering = ('-timestamp',)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, related_name='user', on_delete=models.SET_NULL, blank=True, null=True, db_index=True)
    ip_address = models.GenericIPAddressField("IP Address", null=True, db_index=True)
    timestamp = models.DateTimeField(db_index=True)
    module = models.CharField(max_length=255, db_index=True)
    action = models.CharField(max_length=255, db_index=True)
    message = models.TextField()