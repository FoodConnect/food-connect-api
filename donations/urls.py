from django.urls import path, include
from rest_framework import routers
from .views import DonationViewSet

router = routers.DefaultRouter()
router = routers.DefaultRouter()
router.register(r'donations', DonationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]