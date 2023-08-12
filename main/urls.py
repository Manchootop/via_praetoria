from django.urls import path
from .views import StoreView, CartView, CheckoutView

urlpatterns = [
    path('store/', StoreView.as_view(), name='store'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
