from django.contrib import admin
from .models import Message, Headers, SpamReport, MailscannerReport, RblReport, McpReport

# Register your models here.
admin.site.register(Message)
admin.site.register(Headers)
admin.site.register(SpamReport)
admin.site.register(MailscannerReport)
admin.site.register(RblReport)
admin.site.register(McpReport)