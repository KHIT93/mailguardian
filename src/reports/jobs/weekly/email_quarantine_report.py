from django_extensions.management.jobs import WeeklyJob
from mail.models import Setting
from core.models import User
from django.conf import settings
from .email_reports import QuarantinedEmailReport

class Job(WeeklyJob):
    help = 'Weekly job for sending weekly quarantine reports to users and administrators'

    def execute(self):
        show_all_messages = not Setting.objects.filter(key='quarantine.report.non_spam.hide').get().value
        report = QuarantinedEmailReport(show_all_messages, 7)
        report.process(User.objects.filter(daily_quarantine_report=True))
