from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartedDonation, Order, Donation, CartStatus, OrderedDonation

from users.models import UserRole, User, Charity

from .serializers import CartSerializer, CartedDonationSerializer, OrderSerializer, OrderedDonationSerializer

from .permissions import IsOrderOwner, IsCartOwner

#for carting/order logic
from django.http import JsonResponse
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import get_user_model
import json


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.none()  # default queryset to avoid DRF assertion error
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCartOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            
            if hasattr(user, 'charity'):
                return Cart.objects.filter(charity=user.charity)
            
            elif hasattr(user, 'donor'):
                return Cart.objects.filter(carted_donations__donation__donor=user.donor).distinct()
        return Cart.objects.none()

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
       
        user = request.user

        if user.role != UserRole.CHARITY.value:
            return Response({'error': 'Only charities can add items to cart'}, status=status.HTTP_403_FORBIDDEN)

        charity = get_object_or_404(Charity, user=user)

        donation_id = request.data.get('donation_id')
        quantity = request.data.get('quantity', 0)

        try:
            donation = Donation.objects.get(pk=donation_id)

            if donation.remaining_inventory < quantity:
                return Response({'error': 'Not enough stock available'}, status=status.HTTP_400_BAD_REQUEST)

            cart, _ = Cart.objects.get_or_create(charity=charity, status=CartStatus.CARTED.value)

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

        if user.role != UserRole.CHARITY.value:
            return Response({'error': 'Only charities can update items in the cart'}, status=status.HTTP_403_FORBIDDEN)

        cart = get_object_or_404(Cart, id=pk)

        charity = get_object_or_404(Charity, id=cart.charity_id)

        donation_id = request.data.get('donation_id')
        quantity_to_update = int(request.data.get('quantity', 0))

        try:
        # Retrieve the carted donation for the specified donation_id AND cart
            carted_donation = CartedDonation.objects.get(cart_id=cart.id, donation_id=donation_id)

            if quantity_to_update > 0:
                carted_donation.quantity = quantity_to_update
                carted_donation.save()
            else:
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

        if user.role != UserRole.CHARITY.value:
            return Response({'error': 'Only charities can checkout'}, status=status.HTTP_403_FORBIDDEN)

        charity = get_object_or_404(Charity, user=user)

        order = Order.objects.create(charity=charity)

        donation_receipts = []

        cart.status = CartStatus.ORDERED.value
        cart.save()

        for carted_donation in cart.carteddonation_set.all():
            donation = carted_donation.donation
            quantity = carted_donation.quantity

            OrderedDonation.objects.create(order=order, donation=donation, quantity=quantity)

            donor_business_name = donation.donor.user.business_name
            donor_ein_number = donation.donor.user.ein_number
        
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

            donation_receipts.append(donation_receipt)

            print("Donation Receipts List:", donation_receipts)

        try:
            order.donation_receipt = json.dumps(donation_receipts)
            order.save()
        except Exception as e:
            print("Error occurred while saving donation receipts:", str(e))

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
    queryset = Order.objects.none()  # default queryset to avoid DRF assertion error
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]
    # filtering orders based on charity user OR donor that has a donation in the order
    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:

            if hasattr(user, 'charity'):
                return Order.objects.filter(charity=user.charity)

            elif hasattr(user, 'donor'):
            
                return Order.objects.filter(ordered_donations__donation__donor__user=user.donor.user).distinct()

        return Order.objects.none()

    # Retrieve Ordered donation information under specific order ID
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class OrderedDonationViewSet(viewsets.ModelViewSet):
    queryset = OrderedDonation.objects.all()
    serializer_class = OrderedDonationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if hasattr(user, 'donor'):
            
            return OrderedDonation.objects.filter(donation__donor__user=user.donor.user).select_related('order')

        elif hasattr(user, 'charity'):
            
            return OrderedDonation.objects.filter(order__charity__user=user.charity.user).select_related('order')
        else:
            return OrderedDonation.objects.none()