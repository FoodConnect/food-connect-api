"""
URL configuration for food_connect_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from food_connect_app.views import UserViewSet, CharityViewSet, DonorViewSet, DonationViewSet, CartViewSet, CartedDonationViewSet, OrderViewSet, CategoryViewSet, DonationCategoryViewSet, ClaimedInventory

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'charities', CharityViewSet)
router.register(r'donors', DonorViewSet)
router.register(r'donations', DonationViewSet)
router.register(r'carts', CartViewSet)
router.register(r'carted_donations', CartedDonationViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'donation_categories', DonationCategoryViewSet)
router.register(r'claimed_inventory', ClaimedInventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Add other paths as needed
]

