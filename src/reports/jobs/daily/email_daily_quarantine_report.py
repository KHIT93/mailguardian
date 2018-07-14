from django_extensions.management.jobs import DailyJob
from core.models import User, Setting, MailScannerHost
from django.conf import settings
from reports.email_reports import QuarantinedEmailReport

class Job(DailyJob):
    help = 'Daily job for sending daily quarantine reports to users and administrators'

    def execute(self):
        # Find out if we should run anything at all
        run_daily = Setting.objects.filter(key='quarantine.report.daily').get().value
        host_count = MailScannerHost.objects.count()
        multi_node = True if host_count > 0 else False
        if run_daily and (multi_node and not settings.API_ONLY):
            show_all_messages = not Setting.objects.filter(key='quarantine.report.non_spam.hide').get().value
            report = QuarantinedEmailReport(show_all_messages, 1)
            report.process(User.objects.filter(daily_quarantine_report=True))
