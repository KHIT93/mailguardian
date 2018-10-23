from django_extensions.management.jobs import WeeklyJob
from core.models import User, Setting, MailScannerHost
from django.conf import settings
from reports.email_reports import QuarantinedEmailReport
from django.utils.translation import gettext_lazy as _

class Job(WeeklyJob):
    help = _('Weekly job for sending weekly quarantine reports to users and administrators')

    def execute(self):
        run_weekly = Setting.objects.filter(key='quarantine.report.weekly').get().value
        host_count = MailScannerHost.objects.count()
        multi_node = True if host_count > 0 else False
        if run_weekly and (multi_node and not settings.API_ONLY):
            show_all_messages = not Setting.objects.filter(key='quarantine.report.non_spam.hide').get().value
            report = QuarantinedEmailReport(show_all_messages, 7)
            report.process(User.objects.filter(weekly_quarantine_report=True))
