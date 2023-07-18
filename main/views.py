from django.shortcuts import render
from django.views.generic import TemplateView


class Demo(TemplateView):
    template_name = 'dashboard.html'