# from django.contrib.auth import get_user_model
# from django.core.validators import MinValueValidator
# from django.db import models
# from django.db.models import CASCADE, ForeignKey, CharField, ImageField, \
#     FloatField, IntegerField, TextField, TextChoices, BooleanField, SET_NULL
# from mptt.fields import TreeForeignKey
# from mptt.models import MPTTModel
#
# from main.models.product_models import Product
# from shared.functions import upload_other_images_product_url
# from shared.models import TimeBaseModel
#
# UserModel = get_user_model()
#
#
# class Category(TimeBaseModel):
#     CATEGORY_NAME_MAX_LENGTH = 40
#
#     name = CharField(
#         max_length=CATEGORY_NAME_MAX_LENGTH
#     )
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         db_table = 'category'
#         verbose_name_plural = "Categories"
#
#
# class SubCategory(TimeBaseModel):
#     SUB_CATEGORY_MAX_LENGTH = 40
#
#     name = CharField(
#         max_length=SUB_CATEGORY_MAX_LENGTH
#     )
#     category = ForeignKey(
#         Category,
#         on_delete=models.CASCADE,
#     )
#
#     def __str__(self):
#         return f'{self.category.name} --> {self.name}'
#
#     class Meta:
#         db_table = 'sub_category'
#         verbose_name_plural = "Sub Categories"
#
#
# class ProductImage(TimeBaseModel):
#     product = ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#     )
#     image = ImageField(
#         upload_to=upload_other_images_product_url
#     )
#
#     class Meta:
#         db_table = 'images'
#
#
# class ProductRating(TimeBaseModel):
#     product = ForeignKey(
#         Product,
#         on_delete=models.CASCADE
#     )
#     rating = IntegerField(
#         default=0
#     )
#     user = ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return f"{self.product} {self.rating} {self.user}"
#
#     class Meta:
#         db_table = 'rating'
#
#
# class ProductComment(TimeBaseModel, MPTTModel):
#     COMMENT_TITLE_MAX_LENGTH = 250
#     COMMENT_TEXT_MAX_LENGTH = 1500
#
#     product = ForeignKey(
#         Product,
#         on_delete=models.CASCADE
#     )
#     title = CharField(
#         max_length=COMMENT_TITLE_MAX_LENGTH
#     )
#
#     text = TextField(
#         max_length=COMMENT_TEXT_MAX_LENGTH
#     )
#     user = ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE
#     )
#     parent = TreeForeignKey(
#         'self',
#         CASCADE,
#         'children',
#         null=True,
#         blank=True
#     )
#
#     is_active = BooleanField(default=False)
#
#     def __str__(self):
#         return f"{self.user} {self.product}"
#
#     class MPTTMeta:
#         order_insertion_by = ['title']
#
#     def children(self):
#         return ProductComment.objects.filter(parent=self)
#
#     @property
#     def is_parent(self):
#         if self.parent is not None:
#             return False
#         return True
#
#     class Meta:
#         db_table = 'comments'
#
#
# class Order(models.Model):
#     customer = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False)
#     transaction_id = models.CharField(max_length=100, null=True)
#
#     def __str__(self):
#         return str(self.id)
#
#
# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     quantity = models.IntegerField(default=0, null=True, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#
# class Cart(TimeBaseModel):
#     user = ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE
#     )
#     count = IntegerField(
#         default=0,
#         validators=(
#             MinValueValidator(0),
#         )
#     )
#     product = ForeignKey(
#         Product,
#         on_delete=models.CASCADE
#     )
#
#     order = ForeignKey(
#         Order,
#         on_delete=models.CASCADE,
#     )
#
#     @property
#     def total_price_of_products(self):
#         return self.product.total_price * self.count
#
#     def __str__(self):
#         return f"{self.user} {self.product} {self.count}"
#
#     class Meta:
#         db_table = 'cart'
#
#
# # class Order(TimeBaseModel):
# #     class StatusChoices(TextChoices):
# #         ordered = 'ordered', 'Ordered'
# #         paid = 'paid', 'Paid'
# #         delivered = 'delivered', 'Delivered'
# #         received = 'received', 'Received'
# #
# #     user = ForeignKey(
# #         UserModel,
# #         on_delete=models.CASCADE
# #     )
# #     count = IntegerField(
# #         default=0
# #     )
# #     product = ForeignKey(
# #         Product,
# #         on_delete=models.SET_NULL,
# #         null=True
# #     )
# #     status = CharField(
# #         max_length=10,
# #         choices=StatusChoices.choices,
# #         default=StatusChoices.ordered
# #     )
# #
# #     def __str__(self):
# #         return f"{self.user} {self.product} {self.status}"
# #
# #     class Meta:
# #         db_table = 'order'
#
#
# class Payment(TimeBaseModel):
#     class PaymentType(TextChoices):
#         click = 'click'
#
#     user = ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE
#     )
#     amount = FloatField(
#         default=0
#     )
#     type = CharField(
#         max_length=85,
#         choices=PaymentType.choices
#     )
#
#     def __str__(self):
#         return f"{self.user} {self.amount}"
#
#     class Meta:
#         db_table = 'payments'
