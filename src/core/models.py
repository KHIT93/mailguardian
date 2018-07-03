from django.db import models
from django.conf import settings
import uuid
from os import listdir
from os.path import isfile, join
import importlib
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from domains.models import Domain
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from auditlog.registry import auditlog
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_domain_admin', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_domain_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    domains = models.ManyToManyField(Domain)
    is_domain_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    daily_quarantine_report = models.BooleanField(default=False)
    weekly_quarantine_report = models.BooleanField(default=False)
    monthly_quarantine_report = models.BooleanField(default=False)
    custom_spam_score = models.FloatField(default=5.0)
    custom_spam_highscore = models.FloatField(default=15.0)
    skip_scan = models.BooleanField(default=False)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def username(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

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

if settings.AUDIT_LOGGING:
    auditlog.register(User)
    auditlog.register(MailScannerConfiguration)
    auditlog.register(Setting)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)