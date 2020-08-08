from django_extensions.management.jobs import MonthlyJob
from core.models import User, Setting, MailScannerHost
from django.conf import settings
from reports.email_reports import QuarantinedEmailReport
from datetime import datetime
from calendar import monthrange
from django.utils.translation import gettext_lazy as _

class Job(MonthlyJob):
    help = 'Monthly job for sending monthly quarantine reports to users and administrators'

    def execute(self):
        # Find out if we should run anything at all
        run_monthly = Setting.objects.filter(key='quarantine.report.monthly').get().value
        host_count = MailScannerHost.objects.count()
        multi_node = True if host_count > 0 else False
        if run_monthly and (multi_node and not settings.API_ONLY):
            period = monthrange(datetime.now().year, datetime.now().month)[1]
            show_all_messages = not Setting.objects.filter(key='quarantine.report.non_spam.hide').get().value
            report = QuarantinedEmailReport(show_all_messages, 30)
            report.process(User.objects.filter(daily_quarantine_report=True))
