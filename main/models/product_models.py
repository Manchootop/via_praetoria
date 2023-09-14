# from ckeditor.fields import RichTextField
# from django.contrib.postgres.fields import HStoreField
# from django.core.validators import MaxValueValidator, MinValueValidator
# from django.db import models
# from django.db.models import FloatField, IntegerField, CharField, \
#     ImageField, ForeignKey
#
# from shared.functions import upload_image_product_url
# from shared.models import TimeBaseModel
#
#
# class Product(TimeBaseModel):
#     PRICE_MAX_VALUE = 102410241024.00
#     PRICE_MIN_VALUE = 0
#
#     name = CharField(
#         max_length=150
#     )
#     description = RichTextField(
#         max_length=400
#     )
#     count = IntegerField(
#         default=0
#     )
#     price = FloatField(
#         default=0,
#         validators=[
#             MaxValueValidator(PRICE_MAX_VALUE),
#             MinValueValidator(PRICE_MIN_VALUE)
#         ])
#     image = ImageField(
#         upload_to=upload_image_product_url
#     )
#     views = IntegerField(
#         default=0
#     )
#
#     category = ForeignKey(
#         'main.SubCategory',
#         on_delete=models.CASCADE,
#         related_name='products_in_category',
#     )
#
    # details = HStoreField(
    #     'details of product', default=dict
    # )
#     sale_percent = IntegerField(
#         default=0,
#         validators=[
#             MaxValueValidator(100),
#             MinValueValidator(0)
#         ])
#
#     def __str__(self):
#         return self.name
#
#     @property
#     def total_price(self):
#         if self.sale_percent > 0:
#             return self.price - self.price * self.sale_percent / 100
#         return self.price
#
#     @property
#     def rating(self):
#         from main.models.handle_order_models import ProductRating
#         product_rating = ProductRating.objects.filter(product_id=self.id)
#         if product_rating.count() > 0:
#             return f"{sum(product_rating.values_list('rating')) / product_rating.count():.2f}"
#         return 0.00
#
#     class Meta:
#         ordering = ('-created_at',)
#         db_table = 'product'
