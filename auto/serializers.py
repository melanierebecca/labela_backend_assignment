
from rest_framework import serializers
from auto.models import Product, CartItem, Cart, Order
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'cart', 'quantity')
        depth = 1


class CartSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'created_at', 'items')
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    customer_first_name = serializers.CharField(source='user.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='user.last_name', read_only=True)
    customer_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = ('cart', 'created_at', 'delivery_time', 'delivery_address', 'delivery_city',
                  'delivery_postal_code', 'country', 'status', 'customer_first_name',
                  'customer_first_name', 'customer_last_name', 'customer_email', 'user')





