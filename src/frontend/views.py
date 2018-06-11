from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import datetime

# Create your views here.
class IndexTemplateView(TemplateView):
    template_name = "mailware/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'app_name': settings.BRAND_NAME, 'app_logo': settings.BRAND_LOGO})

class DashboardApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        # We also need to add an option for changing the data interval
        # when we refactor the UI
        # today = '2017-11-17'
        # interval = ['2017-11-17 21:00:00', '2017-11-17 22:00:00']
        today = datetime.date.today()
        interval = [datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(hours=1)]
        if 'interval' in request.POST:
            if request.POST['interval'] == 'last_hour':
                interval = [datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(hours=1)]
            elif request.POST['interval'] == 'last_day':
                interval = [datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(days=1)]
            elif request.POST['interval'] == 'today':
                interval = [datetime.date.today(), datetime.date.today()]
        result = None
        chart_data = []
        with connection.cursor() as cursor:
            cursor.execute("select count(id) as total, count(CASE WHEN is_spam THEN 1 END) as total_spam, count(CASE WHEN infected THEN 1 END) as total_virus from public.mail_message where timestamp between '{0}'::timestamptz and '{1}'::timestamptz".format(str(interval[0]), str(interval[1])))
            result = cursor.fetchone()

        with connection.cursor() as cursor:
            cursor.execute("select date_trunc('minute', timestamp) as time, count(id) as total, count(CASE WHEN is_spam THEN 1 END) as total_spam, count(CASE WHEN infected THEN 1 END) as total_virus from public.mail_message where timestamp between '{0}'::timestamptz and '{1}'::timestamptz group by time".format(str(interval[0]), str(interval[1])))
            chart_data = cursor.fetchall()
        
        data = {
            'daily_total' : result[0],
            'daily_spam' : result[1],
            'daily_virus' : result[2],
            'chart_data' : chart_data
        }
        return Response(data, status=status.HTTP_200_OK)
