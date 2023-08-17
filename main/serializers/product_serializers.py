from django.db.models import F
from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from main.models.product_models import Product


class ProductModelSerializer(ModelSerializer):
    views = IntegerField(read_only=True)

    class Meta:
        model = Product
        exclude = ('updated_at',)
