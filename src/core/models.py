from django.db import models
from django.conf import settings
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
            print(f)
            module = importlib.import_module('core.fileparsers')
            classname = getattr(module, f.replace('.', ' ').title().replace(' ', '') + 'FileParser')
            print(classname)
            parser = None
            try:
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