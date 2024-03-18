from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# for carting processes
from rest_framework.decorators import action

from .models import User, Charity, Donor, Donation, Cart, CartedDonation, Order, Category, DonationCategory

from .serializers import UserSerializer, CharitySerializer, DonorSerializer, DonationSerializer, CartSerializer, CartedDonationSerializer, OrderSerializer, CategorySerializer, DonationCategorySerializer

# google oauth authentication
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings
# from django.shortcuts import redirect
# from google_auth_oauthlib.flow import Flow
# from .authentication import GoogleAuthentication

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

    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        cart = self.get_object()
        donation_id = request.data.get('donation_id')
        quantity = request.data.get('quantity', 1)
        donation = Donation.objects.get(pk=donation_id)
        if donation.stock < quantity:
            return Response({'error': 'Not enough stock available'}, status=status.HTTP_400_BAD_REQUEST)
        carted_donation = CartedDonation(cart=cart, donation=donation, quantity=quantity)
        carted_donation.save()
        return Response({'message': 'Item added to cart'}, status=status.HTTP_200_OK)

class CartedDonationViewSet(viewsets.ModelViewSet):
    queryset = CartedDonation.objects.all()
    serializer_class = CartedDonationSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def create_order(self, request, pk=None):
        cart = Cart.objects.get(pk=pk)
        carted_donations = CartedDonation.objects.filter(cart=cart)
        if not carted_donations.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(status='Pending')
        for carted_donation in carted_donations:
            order.carted_donations.add(carted_donation)
        carted_donations.delete()
        return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DonationCategoryViewSet(viewsets.ModelViewSet):
    queryset = DonationCategory.objects.all()
    serializer_class = DonationCategorySerializer

# google oauth - authentication
# class GoogleAuthView(APIView):
#     def get(self, request):
#         flow = Flow.from_client_secrets_file(
#             settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
#             scopes=['openid', 'email'],
#             redirect_uri='http://localhost:8000/auth/google/callback')
#         authorization_url, state = flow.authorization_url(
#             access_type='offline',
#             include_granted_scopes='true')
#         request.session['oauth_state'] = state
#         return redirect(authorization_url)

# class GoogleAuthCallbackView(APIView):
#     def get(self, request):
#         flow = Flow.from_client_secrets_file(
#             settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
#             scopes=['openid', 'email'],
#             redirect_uri='http://localhost:8000/auth/google/callback')
#         state = request.session['oauth_state']
#         flow.fetch_token(authorization_response=request.build_absolute_uri(), state=state)
#         token = flow.credentials.id_token
#         # Handle token, e.g., store it in session or use it for authentication
#         return Response({'token': token}, status=status.HTTP_200_OK)
