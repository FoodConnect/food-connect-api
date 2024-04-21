from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import action
from .views import CartViewSet, CartedDonationViewSet, OrderViewSet, OrderedDonationViewSet

router = routers.DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'carted_donations', CartedDonationViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'ordered_donations', OrderedDonationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('carted_donations/cart/<int:pk>/', CartedDonationViewSet.as_view({'get': 'carted_donations_for_cart'}), name='carted_donations_cart'),
    path('carts/add_to_cart/', CartViewSet.as_view({'post': 'add_to_cart'}), name='add_to_cart'),
    path('carts/<int:pk>/remove_from_cart/', CartViewSet.as_view({'post': 'remove_from_cart'}), name='remove_from_cart'),
    path('carts/<int:pk>/checkout/', CartViewSet.as_view({'post': 'checkout'}), name='checkout'),
]