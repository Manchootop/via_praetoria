import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from main.models.product_models import Product
from main.models.handle_order_models import Category, SubCategory, ProductImage, ProductRating, Cart, Order, \
    Payment, ProductComment, OrderItem
from main.serializers.handle_order_serializers import CategorySerializer, \
    SubCategorySerializer, ImagesSerializer, RatingSerializer, CartSerializer, \
    OrderSerializer, PaymentsSerializer, CommentsSerializer
from main.serializers.product_serializers import ProductSerializer
from shared import IsOwnerOrIsAdminOrReadOnly

import json

UserModel = get_user_model()


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


class CartListAPIView(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user  # Use request.user to get the authenticated user
        if user.is_authenticated:
            return Cart.objects.filter(user=user)
        else:
            return Cart.objects.none()

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


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

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(user=self.request.user, product=product, count=1)  # Default count is 1


def get_authenticated_user_from_cookie(request):
    auth_token = request.COOKIES.get('auth_token')  # Change 'auth_token' to 'token'
    print(auth_token)
    if auth_token:
        try:
            user = UserModel.objects.get(token=auth_token)  # Change 'auth_token' to 'token'
            if user.is_authenticated:
                return user
        except UserModel.DoesNotExist:
            pass
    return None


class CartDataAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            cart = {}  # Create an empty cart dictionary

            # You can loop through the Product model data to populate the cart dictionary
            products = Product.objects.all()
            for product in products:
                cart[product.id] = {'quantity': 0}  # Initialize quantity to 0 for each product

            # Update the cart dictionary based on the COOKIES['cart'] data
            try:
                cart_data = json.loads(request.COOKIES['cart'])
                for product_id, quantity in cart_data.items():
                    if product_id in cart:
                        cart[product_id]['quantity'] = quantity
            except:
                print('No cart data found in cookies.')

            items = []
            order = Order()  # Create an empty order object
            order.total = 0
            cart_items = 0

            for product_id, cart_item in cart.items():
                try:
                    quantity = cart_item['quantity']
                    cart_items += quantity

                    product = Product.objects.get(id=product_id)
                    total = (product.price * quantity)
                    order.total += total

                    item = {
                        'id': product.id,
                        'product': {'id': product.id, 'name': product.name, 'price': product.price,
                                    'imageURL': product.imageURL},
                        'quantity': quantity,
                        'digital': product.digital, 'get_total': total,
                    }
                    items.append(item)

                    if not product.digital:
                        order.shipping = True
                except:
                    pass

            order.cart_items = cart_items

        order_serializer = OrderSerializer(order, context={'request': request})
        items_serializer = ProductSerializer(items, many=True, context={'request': request})

        response_data = {
            'cartItems': cart_items,
            'order': order_serializer.data,
            'items': items_serializer.data
        }

        return Response(response_data)


def create_cart_for_user(request):
    user = get_authenticated_user_from_cookie(request)

    if user:
        customer, _ = UserModel.objects.get_or_create(user=user)
    else:
        customer = None

    order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    return order


class StoreAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = get_authenticated_user_from_cookie(self.request)

        if user:
            customer, _ = UserModel.objects.get_or_create(user=user)
            order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        else:
            order = create_cart_for_user(self.request)

        # Now you have the order associated with the user or guest
        # You can proceed to retrieve the order items and update the context
        items = order.orderitem_set.all()

        # Update the order instance with order items
        order.order_items = items

        # Update the context with the order instance
        context = {'order': order}

        return Product.objects.all(), context

    def get(self, request, *args, **kwargs):
        queryset, context = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context=context)
        return Response(serializer.data)


class CartAPIView(RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_object(self):
        user = get_authenticated_user_from_cookie(self.request)

        if user:
            customer = user.customer
            order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        else:
            order = create_cart_for_user(None)

        return order


class CheckoutAPIView(RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_object(self):
        user = get_authenticated_user_from_cookie(self.request)

        if user:
            customer = user.customer
            order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        else:
            order = create_cart_for_user(None)

        return order


class UpdateItemAPIView(APIView):
    def post(self, request):
        data = request.data
        product_id = data.get('productId')
        action = data.get('action')

        if not product_id or not action:
            return Response({'message': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)

        customer = request.user.customer
        product = Product.objects.get(id=product_id)
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)

        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            order_item.quantity += 1
        elif action == 'remove':
            order_item.quantity -= 1

        if order_item.quantity <= 0:
            order_item.delete()
        else:
            order_item.save()

        return Response({'message': 'Item was updated'}, status=status.HTTP_200_OK)


class ProcessOrderAPIView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        transaction_id = datetime.datetime.now().timestamp()
        data = request.data

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            total = float(data['form']['total'])
            order.transaction_id = transaction_id
            order.complete = True  # Mark order as complete
            order.save()
        else:
            return Response({'message': 'User is not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'message': 'Payment submitted'}, status=status.HTTP_200_OK)
