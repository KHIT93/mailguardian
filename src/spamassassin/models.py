from django.db import models
from django.conf import settings
import re, uuid, subprocess

# Create your models here.
class Rule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    score = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)

class RuleDescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField(blank=True, null=True)

    def sync_files(self):
        # Sync spam assassin rule descriptions to database
        # grep -hr '^\s*describe' " . SA_RULES_DIR . ' /usr/share/spamassassin /usr/local/share/spamassassin ' . SA_PREFS . ' /etc/MailScanner/spam.assassin.prefs.conf /opt/MailScanner/etc/spam.assassin.prefs.conf /usr/local/etc/mail/spamassassin /etc/mail/spamassassin /var/lib/spamassassin 2>/dev/null | sort | uniq
        output = subprocess.check_output("/bin/grep -hr '^\s*describe' {0} {1} /etc/MailScanner/spam.assassin.prefs.conf /etc/mail/spamassassin /var/lib/spamassassin 2>/dev/null | /usr/bin/sort | /usr/bin/uniq".format(settings.SA_RULES_DIR, settings.SA_PREF), shell=True)
        descriptions = re.findall(r"^(?:\s*)describe\s+(\S+)\s+(.+)$", output.decode(), re.MULTILINE)
        for match in descriptions:
            if RuleDescription.objects.filter(key=match[0]).first():
                rule = RuleDescription.objects.filter(key=match[0]).first()
                rule.value = match[1]
                rule.save()
            else:
                RuleDescription.objects.get_or_create(key=match[0], value=match[1])