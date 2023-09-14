from django.db.models import F
from rest_framework.fields import IntegerField, ReadOnlyField
from rest_framework.serializers import ModelSerializer

from main.models.product_models import Product
from main.serializers.handle_order_serializers import CategorySerializer, SubCategorySerializer


class ProductSerializer(ModelSerializer):
    views = IntegerField(read_only=True)
    category = CategorySerializer()
    # rating = ReadOnlyField()  # Add this line
    total_price = ReadOnlyField()  # Add this line\
    sub_category = SubCategorySerializer(source='category')

    class Meta:
        model = Product
        exclude = ('updated_at',)
