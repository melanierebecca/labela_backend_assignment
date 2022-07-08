from django.urls import include, path
from rest_framework import routers

# from auto import views
from auto.views import ProductViewSet, CartViewSet, CartItemViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cartitems', CartItemViewSet)
router.register(r'order', OrderViewSet)

cart = CartViewSet.as_view({
    'post': 'create',
    'get': 'retrieve',
})

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', cart),
    path('auto/', include('rest_framework.urls', namespace='rest_framework'))
]