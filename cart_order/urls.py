from django.urls import path, include
from rest_framework import routers
from .views import CartViewSet, CartedDonationViewSet, OrderViewSet, OrderedDonationViewSet

router = routers.DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'carted_donations', CartedDonationViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'ordered_donations', OrderedDonationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('carts/cart_for_current_user/', CartViewSet.as_view({'get': 'cart_for_current_user'}), name='cart_for_current_user'),
    path('carts/add_to_cart/', CartViewSet.as_view({'post': 'add_to_cart'}), name='add_to_cart'),
    path('carts/update/', CartViewSet.as_view({'post': 'update_cart'}), name='update_cart'),
    path('carts/<int:pk>/checkout/', CartViewSet.as_view({'post': 'checkout'}), name='checkout'),
]