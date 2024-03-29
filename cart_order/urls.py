from django.urls import path, include
from rest_framework import routers
from .views import CartViewSet, CartedDonationViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'carted_donations', CartedDonationViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]