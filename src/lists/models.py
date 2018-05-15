import uuid
from django.db import models

class ListEntry(models.Model):
    class Meta:
        db_table = 'list_entries'
        indexes = [
            models.Index(fields=['from_address', 'to_address']),
            models.Index(fields=['from_address', 'listing_type']),
            models.Index(fields=['to_address', 'listing_type']),
        ]
        unique_together = ('from_address', 'to_address', 'listing_type')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_address = models.CharField("From", max_length=511, blank=True, default="", db_index=True)
    to_address = models.CharField("To", max_length=511, blank=True, default="", db_index=True)
    listing_type = models.CharField(max_length=12, choices=(
        ('blacklisted', 'Blacklisted'),
        ('whitelisted', 'Whitelisted')
    ), db_index=True)
