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
        user_filter = ""
        if request.user.is_domain_admin:
            user_filter = ""
        elif not request.user.is_domain_admin and not request.user.is_staff:
            user_filter = " AND (from_address={0}' OR to_address='{0}')".format(request.user.email)
        with connection.cursor() as cursor:
            cursor.execute("select count(m.id) as total, count(CASE WHEN m.is_spam THEN 1 END) as total_spam, count(CASE WHEN m.infected THEN 1 END) as total_virus from public.mail_message as m where m.{field} between '{fromdate}'::timestamptz and '{todate}'::timestamptz{filter}".format(field=field, fromdate=str(interval[0]), todate=str(interval[1]), filter=user_filter))
            result = cursor.fetchone()
        with connection.cursor() as cursor:
            cursor.execute("select date_trunc('{timefield}', m.timestamp) as time, count(m.id) as total, count(CASE WHEN m.is_spam THEN 1 END) as total_spam, count(CASE WHEN m.infected THEN 1 END) as total_virus from public.mail_message as m where m.{field} between '{fromdate}'::timestamptz and '{todate}'::timestamptz{filter} group by time order by time".format(field=field, fromdate=str(interval[0]), todate=str(interval[1]), timefield=timefield, filter=user_filter))
            chart_data = cursor.fetchall()
        
        data = {
            'daily_total' : result[0],
            'daily_spam' : result[1],
            'daily_virus' : result[2],
            'chart_data' : chart_data
        }
        return Response(data, status=status.HTTP_200_OK)
