from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from main.models import Product


class ListProductsView(ListView):
    model = Product
    template_name = 'list-products'
