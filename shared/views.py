from rest_framework.decorators import api_view
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


@api_view(['GET'])
def endpoints(request):
    data = ['/products', '/products/<id>', '/cart', '/orders/get-my-orders', '/category', '/category/<id>'] + [
        '/sub_category', '/sub_category/<id>/', '/products/add-to-cart/<int:product_pk>'
    ]

    return Response(data)


class CRUDViewSet(
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    pass
