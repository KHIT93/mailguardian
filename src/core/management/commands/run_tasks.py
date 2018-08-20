from django.core.management.base import BaseCommand, CommandError
from core.models import ApplicationTask, MailScannerHost
from django.conf import settings
import importlib

class Command(BaseCommand):
    help = 'Run queued tasks'

    def handle(self, *args, **kwargs):
        host_count = MailScannerHost.objects.count()
        multi_node = True if host_count > 0 else False
        tasks = ApplicationTask.objects.all()
        if multi_node and not settings.API_ONLY:
            tasks = tasks.filter(host=None)
        else:
            host = MailScannerHost.objects.filter(hostname=settings.APP_HOSTNAME).first()
            tasks = tasks.filter(host=host)
        for task in tasks:
            task.status_code = 'RUNNING'
            task.save()
            module = importlib.import_module(task.content_type.app_label + '.models')
            model = getattr(module, task.content_type.model)
            obj = model.objects.filter(pk=task.object_pk).first()
            # Execute task.method on obj inside a try-catch
            try:
                action = getattr(obj, task.method)
                result = action(task.params)
                task.status_message = result
                task.status_code = 'COMPLETED'
            except Exception as e:
                # If we encounter and error, store the result on the task and mark it as failed
                task.status_message = e
                task.status_code = 'FAILED'
            # Otherwise mark is as completed and store the result
            task.save()

