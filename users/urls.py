from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, CharityViewSet, DonorViewSet
from .signals import create_profile

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework_simplejwt.views import TokenVerifyView

from .views import UserRegistrationAPIView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'charities', CharityViewSet)
router.register(r'donors', DonorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
]