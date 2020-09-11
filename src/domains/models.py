import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from compliance.registry import datalog

# https://gist.github.com/solusipse/7ed8e1da104baaee3f05

# Create your models here.

# This maps to postfix virtual_mailbox_domains and virtual_transport
class Domain(models.Model):
    class Meta:
        verbose_name = _('domain')
        verbose_name_plural = _('domains')
        ordering = ('-name',)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Name'), max_length=128, unique=True)
    destination = models.CharField(_('Destination'), max_length=128, null=True, blank=True)
    relay_type = models.CharField(_('Relay type'), max_length=64, default='smtp')
    created_timestamp = models.DateTimeField(_('Created on'), auto_now_add=True, auto_now=False)
    updated_timestamp = models.DateTimeField(_('Last updated on'), auto_now=True)
    active = models.BooleanField(_('Active'), default=False)
    catchall = models.BooleanField(_('Catchall'), default=False)
    # For commercial use in order to limit the number of recipient mailboxes that can be created
    allowed_accounts = models.IntegerField(_('Allowed user accounts for domain'), default=-1)
    receive_type = models.CharField(_('Recieve type'), max_length=25, choices=(
        ('load_balanced', _('Load balancing')),
        ('failover', _('Failover'))
    ), default="failover")

    def __str__(self):
        return self.name

datalog.register(model=Domain)