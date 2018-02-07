from django.contrib import admin
from .models import Domain, MailUser

# Register your models here.
admin.site.register(Domain)
admin.site.register(MailUser)