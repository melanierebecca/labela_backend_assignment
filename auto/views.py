from rest_framework import viewsets, permissions, filters
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response

from auto.models import Product, CartItem, Cart, Order
from auto.serializers import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be only viewed.
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [permissions.IsAdminUser | ReadOnly]


class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cart to be created and edited.
    """
    queryset = CartItem.objects.all()
    lookup_field = 'pk'
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cart items to be viewed and edited.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    lookup_url_kwarg = "cart_id"

    def retrieve(self, request, *args, **kwargs):
        cart_id = kwargs.pop('cart_id', None)
        if cart_id:
            items = CartItem.objects.all()
            items = CartItem.objects.filter(cart=cart_id)
            serializer = CartItemSerializer(items, many=True)
            return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        cart_id = request.data.pop('cart')
        product_id = request.data.pop('product')

        def calculate_total(inc):
            current_total = Cart.objects.get(pk=cart_id).total
            new_total = current_total + (inc * product.price)
            return new_total

        filtered_cart_item = CartItem.objects.filter(cart=cart_id, product=product_id)
        quantity = request.data.pop('quantity')
        cart = Cart.objects.get(pk=cart_id)
        product = Product.objects.get(pk=product_id)
        increment = quantity
        if filtered_cart_item.exists():
            increment = int(quantity) - filtered_cart_item[0].quantity
            cart_item = filtered_cart_item[0]
            cart_item.quantity = int(quantity)
            cart_item.save()

        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)
            cart.total = calculate_total(increment)
            cart.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cart to be created and edited.
    """
    serializer_class = OrderSerializer
    filter_fields = {
        'id': ['exact'],
        'status': ['exact']
    }
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def get_queryset(self):
        """
        This view should return a list of all the orders
        for the currently authenticated user.
        """
        user = self.request.user
        orders = Order.objects.filter(user=user)
        return orders
