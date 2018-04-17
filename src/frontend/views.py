from django.shortcuts import render
from django.views.generic import TemplateView
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import datetime

# Create your views here.
class IndexTemplateView(TemplateView):
    template_name = "mailware/index.html"

class DashboardApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        # We also need to add an option for changing the data interval
        # when we refactor the UI
        today = datetime.date.today()
        result = None
        with connection.cursor() as cursor:
            cursor.execute("select count(id) as total, count(CASE WHEN is_spam THEN 1 END) as total_spam, count(CASE WHEN infected THEN 1 END) as total_virus from public.mail_message where date = '{0}'".format(str(today)))
            result = cursor.fetchone()
        data = {
           'daily_total' : result[0],
           'daily_spam' : result[1],
           'daily_virus' : result[2]
        }
        return Response(data, status=status.HTTP_200_OK)
