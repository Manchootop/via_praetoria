from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Product, Order
from django.views.generic import ListView
from .models import Product

class StoreView(ListView):
    template_name = 'store/store.html'
    model = Product
    context_object_name = 'products'


class CartView(TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            # Create empty cart for non-logged in user
            items = []
        context['items'] = items
        return context

class CheckoutView(TemplateView):
    template_name = 'store/checkout.html'
