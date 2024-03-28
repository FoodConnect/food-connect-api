from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import User, Charity, Donor

from .serializers import UserSerializer, CharitySerializer, DonorSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CharityViewSet(viewsets.ModelViewSet):
    queryset = Charity.objects.select_related('user').all()
    serializer_class = CharitySerializer

class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.select_related('user').all()
    serializer_class = DonorSerializer
