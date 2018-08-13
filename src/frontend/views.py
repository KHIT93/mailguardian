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
        join = ""
        if request.user.is_domain_admin:
            domain_ids = [domain.name for domain in request.user.domains.all()]
            join = " INNER JOIN public.domains_domain as fd ON m.from_domain=fd.name INNER JOIN public.domains_domain as td ON m.to_domain=td.name"
            user_filter = " AND (m.from_domain IN ({0}) OR m.to_domain IN ({0}))".format("'" + "','".join(domain_ids) + "'")
        elif not request.user.is_domain_admin and not request.user.is_staff:
            user_filter = " AND (m.from_address='{0}' OR m.to_address='{0}')".format(request.user.email)
        with connection.cursor() as cursor:
            cursor.execute("SELECT count(m.id) as total, count(CASE WHEN m.is_spam THEN 1 END) as total_spam, count(CASE WHEN m.infected THEN 1 END) as total_virus FROM public.mail_message as m{join} where m.{field} between '{fromdate}' and '{todate}'{filter}".format(field=field, fromdate=str(interval[0]), todate=str(interval[1]), filter=user_filter, join=join))
            result = cursor.fetchone()
        with connection.cursor() as cursor:
            cursor.execute("SELECT date_trunc('{timefield}', m.timestamp) as time, count(m.id) as total, count(CASE WHEN m.is_spam THEN 1 END) as total_spam, count(CASE WHEN m.infected THEN 1 END) as total_virus FROM public.mail_message as m{join} where m.{field} between '{fromdate}' and '{todate}'{filter} group by time order by time".format(field=field, fromdate=str(interval[0]), todate=str(interval[1]), timefield=timefield, filter=user_filter, join=join))
            chart_data = cursor.fetchall()
        
        data = {
            'daily_total' : result[0],
            'daily_spam' : result[1],
            'daily_virus' : result[2],
            'chart_data' : chart_data
        }
        return Response(data, status=status.HTTP_200_OK)
