from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    price = models.FloatField(default=0)
    # image_url = models.ImageField(upload_to='cars', null=True)
    image_url = models.CharField(max_length=500)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    total = models.FloatField(default=0.0)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    delivery_time = models.DateField()
    delivery_address = models.CharField(max_length=100)
    delivery_city = models.CharField(max_length=50)
    delivery_postal_code = models.CharField(max_length=8)
    country = models.CharField(max_length=50)
    status = models.CharField(max_length=10, default="PLACED")


class Delivery(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=8)
    country = models.CharField(max_length=50)
