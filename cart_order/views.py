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

            # Find or create a cart for the user's charity
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
    def remove_from_cart(self, request, pk=None):
        cart = self.get_object()
        user = request.user

        # Ensure the authenticated user has the 'charity' role
        if user.role != UserRole.CHARITY.value:
            return Response({'error': 'Only charities can remove items from cart'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the associated Charity object
        charity = get_object_or_404(Charity, user=user)

        donation_id = request.data.get('donation_id')
        quantity_to_remove = int(request.data.get('quantity', 1))

        try:
            # Retrieve the carted donation for the specified donation_id
            carted_donation = CartedDonation.objects.get(cart__charity=charity, donation_id=donation_id)

            # If the requested quantity to remove is greater than the quantity in the cart,
            # simply delete the entire carted donation
            if quantity_to_remove >= carted_donation.quantity:
                carted_donation.delete()
            else:
                # If the requested quantity to remove is less than the quantity in the cart,
                # decrement the carted donation quantity by the requested quantity
                carted_donation.quantity -= quantity_to_remove
                carted_donation.save()

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

        # Update cart status to "ordered"
        cart.status = CartStatus.ORDERED.value
        cart.save()

        # Iterate through carted donations to create ordered donations
        for carted_donation in cart.carteddonation_set.all():
            donation = carted_donation.donation
            quantity = carted_donation.quantity

            # Create ordered donation for the current carted donation
            OrderedDonation.objects.create(order=order, donation=donation, quantity=quantity)

        # Reduce remaining_inventory and increase claimed_inventory on the appropriate Donation models
        for ordered_donation in order.ordered_donations.all():
            donation = ordered_donation.donation
            quantity = ordered_donation.quantity
            donation.remaining_inventory -= quantity
            donation.claimed_inventory += quantity
            donation.save()

        return Response({'message': 'Order processed successfully'}, status=status.HTTP_200_OK)

class CartedDonationViewSet(viewsets.ModelViewSet):
    queryset = CartedDonation.objects.all()
    serializer_class = CartedDonationSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderedDonationViewSet(viewsets.ModelViewSet):
    queryset = OrderedDonation.objects.all()
    serializer_class = OrderedDonationSerializer
