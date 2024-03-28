from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartedDonation, Order

from .serializers import CartSerializer, CartedDonationSerializer, OrderSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartedDonationViewSet(viewsets.ModelViewSet):
    queryset = CartedDonation.objects.all()
    serializer_class = CartedDonationSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
