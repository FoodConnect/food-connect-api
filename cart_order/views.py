from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartedDonation, Order, Donation, CartStatus, OrderedDonation

from users.models import UserRole, User, Charity

from .serializers import CartSerializer, CartedDonationSerializer, OrderSerializer, OrderedDonationSerializer

#for carting/order logic
from django.http import JsonResponse
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import get_user_model
import json


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        # Obtain the authenticated user
        user = request.user

        # Ensure the authenticated user has the 'charity' role
        if user.role != UserRole.CHARITY.value:
            return Response({'error': 'Only charities can add items to cart'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the associated Charity object
        charity = get_object_or_404(Charity, user=user)

        donation_id = request.data.get('donation_id')
        quantity = request.data.get('quantity', 0)

        try:
            donation = Donation.objects.get(pk=donation_id)

            if donation.remaining_inventory < quantity:
                return Response({'error': 'Not enough stock available'}, status=status.HTTP_400_BAD_REQUEST)

            # Find or create a cart for the authenticated user
            cart, _ = Cart.objects.get_or_create(charity=charity, status=CartStatus.CARTED.value)

            # Add the donation to the cart
            carted_donation, created = CartedDonation.objects.get_or_create(cart=cart, donation=donation)
            if not created:
                carted_donation.quantity += int(quantity)
                carted_donation.save()
            else:
                carted_donation.quantity = int(quantity)
                carted_donation.save()

            return Response({'message': 'Item added to cart'}, status=status.HTTP_200_OK)
        except Donation.DoesNotExist:
            return Response({'error': 'Donation not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def update_cart(self, request, pk=None):
        cart = self.get_object()
        user = request.user

        # Ensure the authenticated user has the 'charity' role
        if user.role != UserRole.CHARITY.value:
            return Response({'error': 'Only charities can update items in the cart'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the associated Charity object
        charity = get_object_or_404(Charity, user=user)

        donation_id = request.data.get('donation_id')
        quantity_to_update = int(request.data.get('quantity', 0))

        try:
            # Retrieve the carted donation for the specified donation_id
            carted_donation = CartedDonation.objects.get(cart__charity=charity, donation_id=donation_id)

            if quantity_to_update > 0:
            
                carted_donation.quantity = quantity_to_update
                carted_donation.save()

            else:
            # If requested quantity is 0 or less, remove carted donation
                carted_donation.delete()

            cart.refresh_from_db()
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CartedDonation.DoesNotExist:
            return Response({'error': 'Carted donation not found'}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['post'])
    @transaction.atomic
    def checkout(self, request, pk=None):
        cart = self.get_object()
        user = request.user

        # Ensure the authenticated user has the 'charity' role
        if user.role != UserRole.CHARITY.value:
            return Response({'error': 'Only charities can checkout'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the associated Charity object
        charity = get_object_or_404(Charity, user=user)

        # Create an order for the user associated with the cart
        order = Order.objects.create(charity=charity)

        # Initialize an empty list to store donation receipts
        donation_receipts = []

        # Update cart status to "ordered"
        cart.status = CartStatus.ORDERED.value
        cart.save()

        # Iterate through carted donations to create ordered donations
        for carted_donation in cart.carteddonation_set.all():
            donation = carted_donation.donation
            quantity = carted_donation.quantity

            # Create ordered donation for the current carted donation
            OrderedDonation.objects.create(order=order, donation=donation, quantity=quantity)

            # Access donor information through the user attribute of the Donor model
            donor_business_name = donation.donor.user.business_name
            donor_ein_number = donation.donor.user.ein_number
        
            # Construct donation receipt
            donation_receipt = {
                'donation_id': donation.id,
                'donation_title': donation.title,
                'donor': donor_business_name,
                'donor_ein_number': donor_ein_number,
                'quantity': quantity,
                'address': donation.address,
                'city': donation.city,
                'state': donation.state,
                'zipcode': donation.zipcode
            }

            # Add donation receipt to the list
            donation_receipts.append(donation_receipt)

            print("Donation Receipts List:", donation_receipts)

        try:
            # Convert donation_receipts list to JSON and store it in the receipt field
            order.donation_receipt = json.dumps(donation_receipts)
            order.save()
        except Exception as e:
            # Print or log the error message for debugging
            print("Error occurred while saving donation receipts:", str(e))


        # Reduce remaining_inventory and increase claimed_inventory on the appropriate Donation models
        for ordered_donation in order.ordered_donations.all():
            donation = ordered_donation.donation
            quantity = ordered_donation.quantity
            donation.remaining_inventory -= quantity
            donation.claimed_inventory += quantity
            donation.save()

        return Response({'message': 'Order processed successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def cart_for_current_user(self, request):
        user = request.user
        
        if user.role != UserRole.CHARITY.value:
            return Response({'message': 'User is not associated with any charity'}, status=status.HTTP_404_NOT_FOUND)
        try:
            charity = user.charity
        except Charity.DoesNotExist:
            return Response({'message': 'User is not associated with any charity'}, status=status.HTTP_404_NOT_FOUND)
        
        charity_id = charity.id
        cart = Cart.objects.filter(charity_id=charity_id, status=CartStatus.CARTED.value).first()
        if cart is None:
            return Response({'message': 'No cart found for the current user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

class CartedDonationViewSet(viewsets.ModelViewSet):
    queryset = CartedDonation.objects.all()
    serializer_class = CartedDonationSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    # Retrieve Ordered donation information under specific order ID
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class OrderedDonationViewSet(viewsets.ModelViewSet):
    queryset = OrderedDonation.objects.all()
    serializer_class = OrderedDonationSerializer
