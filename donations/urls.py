from django.urls import path, include
from rest_framework import routers
from .views import DonationViewSet, CategoryViewSet, DonationCategoryViewSet

router = routers.DefaultRouter()
router = routers.DefaultRouter()
router.register(r'donations', DonationViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'donation_categories', DonationCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]