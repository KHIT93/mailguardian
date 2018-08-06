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
    template_name = "mailguardian/index.html"

    def get(self, request, *args, **kwargs):
        if settings.API_ONLY:
            return Response({}, status.HTTP_401_UNAUTHORIZED)
        return render(request, self.template_name, {'app_name': settings.BRAND_NAME, 'app_logo': settings.BRAND_LOGO})

class DashboardApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        today = datetime.datetime.strptime('2018-05-05', '%Y-%m-%d')
        interval = [today, today]
        field = 'timestamp'
        timefield = 'hour'
        if 'interval' in request.data:
            if request.data['interval'] == 'last_hour':
                now = datetime.datetime.now()
                interval = [now - datetime.timedelta(hours=1), now]
                field = 'timestamp'
            elif request.data['interval'] == 'last_day':
                now = datetime.datetime.now()
                interval = [now - datetime.timedelta(days=1), now]
                field = 'timestamp'
                timefield = 'hour'
            elif request.data['interval'] == 'today':
                interval = [today, today + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)]
                field = 'timestamp'
                timefield = 'hour'
            else:
                Response({'interval': 'Invalid interval has been specified'}, status=status.HTTP_400_BAD_REQUEST)
        result = None
        chart_data = []
        with connection.cursor() as cursor:
            cursor.execute("select count(id) as total, count(CASE WHEN is_spam THEN 1 END) as total_spam, count(CASE WHEN infected THEN 1 END) as total_virus from public.mail_message where {field} between '{fromdate}'::timestamptz and '{todate}'::timestamptz".format(field=field, fromdate=str(interval[0]), todate=str(interval[1])))
            result = cursor.fetchone()
        with connection.cursor() as cursor:
            cursor.execute("select date_trunc('{timefield}', timestamp) as time, count(id) as total, count(CASE WHEN is_spam THEN 1 END) as total_spam, count(CASE WHEN infected THEN 1 END) as total_virus from public.mail_message where {field} between '{fromdate}'::timestamptz and '{todate}'::timestamptz group by time order by time".format(field=field, fromdate=str(interval[0]), todate=str(interval[1]), timefield=timefield))
            chart_data = cursor.fetchall()
        
        data = {
            'daily_total' : result[0],
            'daily_spam' : result[1],
            'daily_virus' : result[2],
            'chart_data' : chart_data
        }
        return Response(data, status=status.HTTP_200_OK)
