from rest_framework.decorators import api_view
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


@api_view(['GET'])
def endpoints(request):
    data = [''
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
