from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Product(models.Model):
    title = models.CharField(
        max_length=50,
    )

    price = models.IntegerField(

    )

    description = models.TextField(
        max_length=500,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    date_ordered = models.DateTimeField(
        auto_now_add=True,
    )

    complete = models.BooleanField(
        default=False,
    )

    transaction_id = models.CharField(
        max_length=100,
        null=True,
    )

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
    )

    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL,
        null=True,
    )

    quantity = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )

    date_added = models.DateTimeField(
        auto_now_add=True
    )


class ClientShipAddress(models.Model):
    customer = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
    )

    address = models.CharField(
        max_length=150,
        null=True,
    )

    city = models.CharField(
        max_length=150,
        null=True,
    )
    state = models.CharField(
        max_length=150,
        null=True,
    )
    zipcode = models.CharField(
        max_length=150,
        null=True,
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.address
