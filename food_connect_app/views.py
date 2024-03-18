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

        try:
            carted_donation = cart.carted_donations.get(donation__id=donation_id)
            carted_donation.quantity += int(quantity)
            carted_donation.save()
        except CartedDonation.DoesNotExist:
            carted_donation = CartedDonation.objects.create(cart=cart, donation_id=donation_id, quantity=quantity)

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_from_cart(self, request, pk=None):
        cart = self.get_object()
        donation_id = request.data.get('donation_id')

        try:
            carted_donation = cart.carted_donations.get(donation__id=donation_id)
            if carted_donation.quantity > 1:
                carted_donation.quantity -= 1
                carted_donation.save()
            else:
                carted_donation.delete()
        except CartedDonation.DoesNotExist:
            pass

        serializer = CartSerializer(cart)
        return Response(serializer.data)

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
        
        # Calculate total inventory changes
        total_inventory_changes = {}
        for carted_donation in carted_donations:
            donation = carted_donation.donation
            if donation.id not in total_inventory_changes:
                total_inventory_changes[donation.id] = carted_donation.quantity
            else:
                total_inventory_changes[donation.id] += carted_donation.quantity
        
        # Update inventory levels for each donation
        for donation_id, quantity in total_inventory_changes.items():
            donation = Donation.objects.get(pk=donation_id)
            donation.claimed_inventory += quantity
            donation.remaining_inventory -= quantity
            donation.save()

        # Create the order
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
