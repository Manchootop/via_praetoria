from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from main.models.product_models import Product
from main.models.handle_order_models import Category, SubCategory, ProductImage, ProductRating, Cart, Order, \
    Payment, ProductComment
from main.serializers.handle_order_serializers import CategorySerializer, \
    SubCategorySerializer, ImagesSerializer, RatingSerializer, CartSerializer, \
    OrderSerializer, PaymentsSerializer, CommentsSerializer
from shared import IsOwnerOrIsAdminOrReadOnly


class CategoryReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ImagesModelListAPIView(ListAPIView):
    serializer_class = ImagesSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))


class ImagesModelDetailAPIView(RetrieveAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ImagesSerializer


class RatingModelViewSet(ModelViewSet):
    queryset = ProductRating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsOwnerOrIsAdminOrReadOnly,)

    def get_queryset(self):
        return ProductRating.objects.filter(user_id=self.request.user.pk)


class CartModelViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsOwnerOrIsAdminOrReadOnly,)

    def get_queryset(self):
        return Cart.objects.filter(user_id=self.request.user.pk)


class OrderReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.pk)


class PaymentsViewSet(ModelViewSet):
    serializer_class = PaymentsSerializer
    permission_classes = (IsOwnerOrIsAdminOrReadOnly,)

    def get_queryset(self):
        return Payment.objects.filter(user_id=self.request.user.pk)


class CommentsListAPIView(ListAPIView):
    serializer_class = CommentsSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        try:
            Product.objects.get(id=self.kwargs.get('product_pk'))
        except ObjectDoesNotExist:
            raise NotFound(f"Product with {self.kwargs.get('product_pk')}-id is not found", HTTP_404_NOT_FOUND)
        return ProductComment.objects.filter(product_id=self.kwargs.get('product_pk'))


class CommentsCreateAPIView(CreateAPIView):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product_pk'] = self.kwargs.get('product_pk')
        return context

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CommentsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsSerializer
    permission_classes = (IsOwnerOrIsAdminOrReadOnly,)

    def get_queryset(self):
        return ProductComment.objects.filter(product_id=self.kwargs.get('product_pk'))


class AddProductToCartView(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(user=self.request.user, product=product, count=1)  # Default count is 1
