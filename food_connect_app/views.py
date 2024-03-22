from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# for carting & order processes
from rest_framework.decorators import action
from django.db import transaction

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

def generate_receipt(order):
    receipt_content = ""
    carted_donations = CartedDonation.objects.filter(order=order)
    for carted_donation in carted_donations:
        donation = carted_donation.donation
        quantity = carted_donation.quantity
        receipt_content += f"Donation: {donation.title}, Quantity: {quantity}\n"
    return receipt_content

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

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        user = request.user
        donation_id = request.data.get('donation_id')
        quantity = request.data.get('quantity', 0)

        try:

            # Retrieve donation information
            donation = Donation.objects.get(pk=donation_id)
            total_inventory = donation.total_inventory
            claimed_inventory = donation.claimed_inventory

            # Calculate available inventory
            available_inventory = total_inventory - claimed_inventory

            # Check if requested quantity exceeds available inventory
            if quantity > available_inventory:
                return Response({'error': 'Not enough stock available'}, status=status.HTTP_400_BAD_REQUEST)

            # Find or create a cart for the user
            cart = Cart.objects.filter(charity__user=user, status=CartStatus.CARTED.value).first()
            if not cart:
                charity = Charity.objects.get(user=user)
                cart = Cart.objects.create(charity=charity, status=CartStatus.CARTED.value)

            # Add the donation to the cart
            carted_donation, created = CartedDonation.objects.get_or_create(cart=cart, donation=donation)
            if not created:
                carted_donation.quantity += int(quantity)
                carted_donation.save()

            return Response({'message': 'Item added to cart'}, status=status.HTTP_200_OK)
        except Donation.DoesNotExist:
            return Response({'error': 'Donation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def remove_from_cart(self, request, pk=None):
        cart = self.get_object()
        donation_id = request.data.get('donation_id')

        try:
        # Retrieve the carted donation associated with the specified donation_id
            carted_donation = CartedDonation.objects.get(cart=cart, donation_id=donation_id)
        
            if carted_donation.quantity > 1:
                carted_donation.quantity -= 1
                carted_donation.save()
            else:
                carted_donation.delete()
            
            # Optionally, refresh the cart to reflect changes in the database
            cart.refresh_from_db()

            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CartedDonation.DoesNotExist:
        # If the carted donation does not exist, return an error response
            return Response({'error': 'Carted donation not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    @transaction.atomic  # Use atomic transaction to ensure consistency
    def checkout(self, request, pk=None):
        cart = self.get_object()

        # Create an order
        order = Order.objects.create(charity=cart.charity)

        # Update cart status to "ordered"
        cart.status = CartStatus.ORDERED.value  # Use enum value directly
        cart.save()

        # Reduce remaining_inventory on the appropriate Donation models
        carted_donations = CartedDonation.objects.filter(cart=cart)
        for carted_donation in carted_donations:
            donation = carted_donation.donation
            quantity = carted_donation.quantity

            # Reduce remaining_inventory
            donation.remaining_inventory -= quantity
            donation.save()

        # Generate receipt and store it in the order
        receipt_content = generate_receipt(order)
        order.donation_receipt = receipt_content
        order.save()

        return Response({'message': 'Order processed successfully'}, status=status.HTTP_200_OK)

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
