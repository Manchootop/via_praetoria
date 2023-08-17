from django.urls import path, include
from rest_framework import routers

from main.views.handle_order_views import RatingModelViewSet, CartModelViewSet, OrderReadOnlyViewSet, \
    CategoryReadOnlyModelViewSet, SubCategoryReadOnlyModelViewSet, ImagesModelListAPIView, ImagesModelDetailAPIView, \
    CommentsListAPIView, CommentsCreateAPIView, CommentsRetrieveUpdateDestroyAPIView, AddProductToCartView
from main.views.product_views import ProductReadOnlyModelViewSet
from shared.views import endpoints

router = routers.SimpleRouter()
router.register('products', ProductReadOnlyModelViewSet, 'product')
router.register('rating', RatingModelViewSet, 'rating')
router.register('cart', CartModelViewSet, 'cart')
router.register('orders/get-my-orders', OrderReadOnlyViewSet, 'order')
router.register('category', CategoryReadOnlyModelViewSet, 'category')
router.register('sub_category', SubCategoryReadOnlyModelViewSet, 'sub_category')

urlpatterns = [
    path('', include(router.urls)),
    path('', endpoints, name='endpoints'),

    # product-images
    path('products/<int:product_pk>/images/', ImagesModelListAPIView.as_view(), name='images-list'),
    path('products/<int:product_pk>/images/<int:pk>/', ImagesModelDetailAPIView.as_view(), name='images-detail'),

    # product-comments
    path('products/<int:product_pk>/comments/', CommentsListAPIView.as_view(), name='comments-list'),
    path('products/<int:product_pk>/comments/create/', CommentsCreateAPIView.as_view(), name='comments-create'),
    path('products/<int:product_pk>/comments/<int:pk>/', CommentsRetrieveUpdateDestroyAPIView.as_view(),
         name='comments-detail'),

    path('products/add-to-cart/<int:product_pk>/', AddProductToCartView.as_view(), name='add-to-cart'),
]
