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
    path('carts/add_to_cart/', CartViewSet.as_view({'post': 'add_to_cart'}), name='add_to_cart'),
    path('carts/<int:pk>/remove_from_cart/', CartViewSet.as_view({'post': 'remove_from_cart'}), name='remove_from_cart'),
    path('carts/<int:pk>/checkout/', CartViewSet.as_view({'post': 'checkout'}), name='checkout'),
]