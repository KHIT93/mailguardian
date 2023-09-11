from django.db import models
from django.conf import settings
import re
import uuid
import invoke
from django.utils.translation import gettext_lazy as _
from compliance.registry import datalog

# Create your models here.
class Rule(models.Model):
    class Meta:
        verbose_name = _('rule')
        verbose_name_plural = _('rules')
        ordering = ('name',)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Name'), max_length=255, unique=True)
    score = models.DecimalField(_('Score'), default=0.00, max_digits=7, decimal_places=2)

class RuleDescription(models.Model):
    class Meta:
        verbose_name = _('rule description')
        verbose_name_plural = _('rule descriptions')
        ordering = ('key',)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(_('Key'), max_length=255, unique=True)
    value = models.TextField(_('Value'), blank=True, null=True)

    def sync_files(self):
        # Sync spam assassin rule descriptions to database
        # grep -hr '^\s*describe' " . SA_RULES_DIR . ' /usr/share/spamassassin /usr/local/share/spamassassin ' . SA_PREFS . ' /etc/MailScanner/spam.assassin.prefs.conf /opt/MailScanner/etc/spam.assassin.prefs.conf /usr/local/etc/mail/spamassassin /etc/mail/spamassassin /var/lib/spamassassin 2>/dev/null | sort | uniq
        result = invoke.run("/bin/grep -hr '^\s*describe' {0} {1} /etc/MailScanner/spam.assassin.prefs.conf /etc/mail/spamassassin /var/lib/spamassassin 2>/dev/null | /usr/bin/sort | /usr/bin/uniq".format(settings.SA_RULES_DIR, settings.SA_PREF), hide=True)
        output = result.stdout
        descriptions = re.findall(r"^(?:\s*)describe\s+(\S+)\s+(.+)$", output.decode(), re.MULTILINE)
        for match in descriptions:
            if RuleDescription.objects.filter(key=match[0]).first():
                rule = RuleDescription.objects.filter(key=match[0]).first()
                rule.value = match[1]
                rule.save()
            else:
                RuleDescription.objects.get_or_create(key=match[0], value=match[1])

datalog.register(model=Rule)
datalog.register(model=RuleDescription)