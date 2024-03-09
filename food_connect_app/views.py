from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import User, Charity, Donor, Donation, Cart, CartedDonation, Order, Category, DonationCategory, ClaimedInventory

from .serializers import UserSerializer, CharitySerializer, DonorSerializer, DonationSerializer, CartSerializer, CartedDonationSerializer, OrderSerializer, CategorySerializer, DonationCategorySerializer, ClaimedInventorySerializer

#authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
from .authentication import GoogleAuthentication

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CharityViewSet(viewsets.ModelViewSet):
    queryset = Charity.objects.select_related('user').all()
    serializer_class = CharitySerializer

class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.select_related('user').all()
    serializer_class = DonorSerializer

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartedDonationViewSet(viewsets.ModelViewSet):
    queryset = CartedDonation.objects.all()
    serializer_class = CartedDonationSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DonationCategoryViewSet(viewsets.ModelViewSet):
    queryset = DonationCategory.objects.all()
    serializer_class = DonationCategorySerializer

class ClaimedInventoryViewSet(viewsets.ModelViewSet):
    queryset = ClaimedInventory.objects.all()
    serializer_class = ClaimedInventorySerializer

# authentication
class GoogleAuthView(APIView):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
            scopes=['openid', 'email'],
            redirect_uri='http://localhost:8000/auth/google/callback')
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')
        request.session['oauth_state'] = state
        return redirect(authorization_url)

class GoogleAuthCallbackView(APIView):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
            scopes=['openid', 'email'],
            redirect_uri='http://localhost:8000/auth/google/callback')
        state = request.session['oauth_state']
        flow.fetch_token(authorization_response=request.build_absolute_uri(), state=state)
        token = flow.credentials.id_token
        # Handle token, e.g., store it in session or use it for authentication
        return Response({'token': token}, status=status.HTTP_200_OK)
