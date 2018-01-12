import uuid
from django.db import models

class ListEntry(models.Model):
    class Meta:
        db_table = 'list_entries'
        indexes = [
            models.Index(fields=['from_address', 'from_domain']),
            models.Index(fields=['to_address', 'to_domain']),
            models.Index(fields=['from_address', 'to_address']),
            models.Index(fields=['from_address', 'to_domain']),
            models.Index(fields=['to_address', 'from_domain']),
            models.Index(fields=['listing_type', 'from_domain']),
            models.Index(fields=['from_address', 'listing_type']),
            models.Index(fields=['listing_type', 'to_domain']),
        ]
        unique_together = ('from_address', 'from_domain', 'to_address', 'to_domain', 'from_ip_address', 'to_ip_address')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_address = models.CharField("From", max_length=511, blank=True, default="", db_index=True)
    to_address = models.CharField("To", max_length=511, blank=True, default="", db_index=True)
    from_domain = models.CharField(max_length=255, blank=True, default="", db_index=True)
    to_domain = models.CharField(max_length=255, blank=True, default="", db_index=True)
    from_ip_address = models.GenericIPAddressField("IP Address", blank=True, null=True, default="", db_index=True)
    to_ip_address = models.GenericIPAddressField("IP Address", blank=True, null=True, default="", db_index=True)
    listing_type = models.CharField(max_length=12, choices=(
        ('blacklisted', 'Blacklisted'),
        ('whitelisted', 'Whitelisted')
    ), db_index=True)
