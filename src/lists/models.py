import uuid
from django.db import models
from auditlog.registry import auditlog
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class ListEntry(models.Model):
    class Meta:
        db_table = 'list_entries'
        indexes = [
            models.Index(fields=['from_address', 'to_address']),
            models.Index(fields=['from_address', 'listing_type']),
            models.Index(fields=['to_address', 'listing_type']),
        ]
        unique_together = ('from_address', 'to_address', 'to_domain', 'listing_type')
        verbose_name = _('listing entry')
        verbose_name_plural = _('listing entries')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_address = models.CharField(_("From"), max_length=511, blank=True, default="", db_index=True)
    to_address = models.CharField(_("To"), max_length=511, blank=True, default="", db_index=True)
    to_domain = models.CharField(_("To"), max_length=255, null=True, blank=True, default="", db_index=True)
    listing_type = models.CharField(_('Listing type'), max_length=12, choices=(
        ('blacklisted', _('Blacklisted')),
        ('whitelisted', _('Whitelisted'))
    ), db_index=True)

    def save(self, *args, **kwargs):
        if '@' in self.to_address:
            self.to_domain = self.to_address.split('@')[:1]
        super(ListEntry, self).save(*args, **kwargs)

if settings.AUDIT_LOGGING:
    auditlog.register(ListEntry)