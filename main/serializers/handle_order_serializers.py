from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer

from main.models.handle_order_models import Category, SubCategory, ProductImage, ProductRating, ProductComment, \
    Cart, Order, Payment
from shared.serializers import GetEmailSerializer


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ImagesSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    class Meta:
        model = ProductRating
        fields = '__all__'


class CommentsSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['user'] = GetEmailSerializer(instance.user).data
        return represent

    def save(self, **kwargs):
        kwargs['product_id'] = self.context['product_pk']
        return super().save(**kwargs)

    @staticmethod
    def get_reply_count(obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    @staticmethod
    def get_author(obj):
        return obj.author.first_name

    class Meta:
        model = ProductComment
        exclude = ('is_active', 'product',)


class CommentsListSerializer(ModelSerializer):
    class Meta:
        model = ProductComment
        fields = '__all__'


class CartSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
