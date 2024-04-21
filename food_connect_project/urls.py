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

from django.contrib import admin
from django.urls import path, include
from donations.urls import router as donations_router
from users.urls import router as users_router
from cart_order.urls import router as cart_order_router

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework_simplejwt.views import TokenVerifyView

from users.views import UserRegistrationAPIView
from cart_order.views import CartViewSet, CartedDonationViewSet, OrderViewSet

from rest_framework.decorators import action

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(donations_router.urls)),
    path('', include(users_router.urls)),
    path('', include(cart_order_router.urls)),
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path('carts/add_to_cart/', CartViewSet.as_view({'post': 'add_to_cart'}), name='add_to_cart'),
    path('carts/<int:pk>/remove_from_cart/', CartViewSet.as_view({'post': 'remove_from_cart'}), name='remove_from_cart'),
    path('carts/<int:pk>/checkout/', CartViewSet.as_view({'post': 'checkout'}), name='checkout'),
    path('carted_donations/cart/<int:pk>/', CartedDonationViewSet.as_view({'get': 'carted_donations_for_cart'}), name='carted_donations_cart'),
]