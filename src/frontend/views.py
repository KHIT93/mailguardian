from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class IndexTemplateView(TemplateView):
    template_name = "mailware/index.html"