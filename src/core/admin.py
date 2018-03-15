from django.contrib import admin
from .models import MailScannerConfiguration, SpamAssassinConfiguration, Setting

# Register your models here.
admin.site.register(MailScannerConfiguration)
admin.site.register(SpamAssassinConfiguration)
admin.site.register(Setting)