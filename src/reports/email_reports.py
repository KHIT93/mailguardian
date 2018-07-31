from mail.models import Message
from core.models import User, Setting
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Q
import os

class QuarantinedEmailReport:
    show_all_messages = False
    from_email = None
    subject = None
    period = 0

    def __init__(self, show_all_messages, period, from_email=None, subject=None, *args, **kwargs):
        self.show_all_messages = show_all_messages
        self.from_email = from_email if from_email else Setting.objects.filter(key='quarantine.report.from').get().value
        self.subject = subject if subject else Setting.objects.filter(key='quarantine.report.subject').get().value
        self.period = period

    def process(self, queryset):
        styles = ""
        with open(os.path.join(settings.ASSETS_DIR, 'dist', 'css', 'app.css')) as f:
            styles = f.read()
        for user in queryset:
            messages = Message.objects.filter(date__gt=datetime.today() - timedelta(days=self.period+1), date__lt=datetime.today())
            messages = messages.filter(Q(from_address=user.email) | Q(to_address=user.email))
            if not self.show_all_messages:
                messages = messages.filter(Q(is_spam=True) | Q(blacklisted=True) | Q(is_mcp=True) | Q(is_rbl_listed=True) | Q(infected=True))
            
            context = {
                'brand_name': settings.BRAND_NAME,
                'brand_tagline': settings.BRAND_TAGLINE,
                'messages': messages,
                'period': self.period,
                'message_count': messages.count(),
                'retention_days': settings.QUARANTINE_RETENTION,
                'domain': settings.APP_HOSTNAME if settings.APP_HOSTNAME else 'localhost',
                'protocol': 'https' if settings.SECURE_SSL_REDIRECT else 'http',
                'styles': styles,
                'show_all': self.show_all_messages
            }
            to_email = user.email
            plaintext = render_to_string('quarantine_report.txt', context)
            html = get_template('quarantine_report.html').render(context)
            email = EmailMultiAlternatives(self.subject, plaintext, self.from_email, [to_email])
            email.attach_alternative(html, "text/html")
            email.send()